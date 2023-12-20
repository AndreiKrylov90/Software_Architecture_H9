from flask import Flask, jsonify, request
from flasgger import Swagger

from models.weather_forecast_holder import WeatherForecastHolder
from controllers.weather_controller import WeatherController
from models.weather import WeatherForecast

app = Flask(__name__)
Swagger(app)

weather_controller = WeatherController(WeatherForecastHolder())

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
