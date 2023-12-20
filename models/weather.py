class WeatherForecast:
    def __init__(self, date, celsius):
        self.date = date
        self.celsius = celsius
        self.fahrenheit = self.calculate_fahrenheit(celsius)

    def calculate_fahrenheit(self, celsius):
        return (celsius * 9/5) + 32