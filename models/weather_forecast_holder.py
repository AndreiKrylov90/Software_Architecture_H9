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


