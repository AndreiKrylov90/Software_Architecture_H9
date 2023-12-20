from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

class WeatherForecast:
    def __init__(self, date, celsius):
        self.date = date
        self.celsius = celsius
        self.fahrenheit = self.calculate_fahrenheit(celsius)

    def calculate_fahrenheit(self, celsius):
        return (celsius * 9/5) + 32

class WeatherForecastHolder:
    def __init__(self):
        self.forecasts = []

    def add_data(self, forecast):
        self.forecasts.append(forecast)

    def get_data_in_interval(self, start_date, end_date):
        return [forecast.__dict__ for forecast in self.forecasts if start_date <= forecast.date <= end_date]

    def update_data_by_date(self, update_date, new_data):
        for forecast in self.forecasts:
            if forecast.date == update_date:
                forecast.celsius = new_data['celsius']
                forecast.fahrenheit = forecast.calculate_fahrenheit(new_data['celsius'])
                break

    def delete_data_by_date(self, delete_date):
        self.forecasts = [forecast for forecast in self.forecasts if forecast.date != delete_date]

class WeatherController:
    def __init__(self, weather_holder):
        self.weather_holder = weather_holder

    def add_data(self, date, celsius):
        new_forecast = WeatherForecast(date, celsius)
        self.weather_holder.add_data(new_forecast)

    def get_data_in_interval(self, start_date, end_date):
        return self.weather_holder.get_data_in_interval(start_date, end_date)

    def update_data_by_date(self, update_date, new_data):
        self.weather_holder.update_data_by_date(update_date, new_data)

    def delete_data_by_date(self, delete_date):
        self.weather_holder.delete_data_by_date(delete_date)

# Инициализируем контроллер и передаем ему WeatherForecastHolder
weather_controller = WeatherController(WeatherForecastHolder())

# Далее, определяем маршруты с использованием контроллера

@app.route('/add_data', methods=['POST'])
def add_data():
    """
    Add Weather Data
    ---
    parameters:
      - name: date
        in: formData
        type: string
        required: true
        description: Date of the weather forecast
      - name: celsius
        in: formData
        type: number
        required: true
        description: Temperature in Celsius
    responses:
      200:
        description: Success
    """
    data = request.form
    date = data['date']
    celsius = float(data['celsius'])
    weather_controller.add_data(date, celsius)
    return jsonify(success=True)

@app.route('/get_data_in_interval', methods=['POST'])
def get_data_in_interval():
    """
    Get Weather Data in Interval
    ---
    parameters:
      - name: start_date
        in: formData
        type: string
        required: true
        description: Start date of the interval
      - name: end_date
        in: formData
        type: string
        required: true
        description: End date of the interval
    responses:
      200:
        description: Weather data in the specified interval
    """
    data = request.form
    start_date = data['start_date']
    end_date = data['end_date']
    result = weather_controller.get_data_in_interval(start_date, end_date)
    return jsonify(result)

@app.route('/update_data_by_date', methods=['POST'])
def update_data_by_date():
    """
    Update Weather Data by Date
    ---
    parameters:
      - name: update_date
        in: formData
        type: string
        required: true
        description: Date to update
      - name: celsius
        in: formData
        type: number
        required: true
        description: New temperature in Celsius
    responses:
      200:
        description: Success
    """
    data = request.form
    update_date = data['update_date']
    new_data = {
        'celsius': float(data['celsius'])
    }
    weather_controller.update_data_by_date(update_date, new_data)
    return jsonify(success=True)

@app.route('/delete_data_by_date', methods=['POST'])
def delete_data_by_date():
    """
    Delete Weather Data by Date
    ---
    parameters:
      - name: delete_date
        in: formData
        type: string
        required: true
        description: Date to delete
    responses:
      200:
        description: Success
    """
    data = request.form
    delete_date = data['delete_date']
    weather_controller.delete_data_by_date(delete_date)
    return jsonify(success=True)

# Добавляем маршрут для корневого URL
@app.route('/')
def home():
    return "Hello, this is the main page of the Weather App."

if __name__ == '__main__':
    app.run(debug=True)
