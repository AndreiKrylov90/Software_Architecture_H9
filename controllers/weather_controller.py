from models.weather_forecast_holder import WeatherForecastHolder
from models.weather import WeatherForecast

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