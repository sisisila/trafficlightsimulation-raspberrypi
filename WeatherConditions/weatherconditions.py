from dataclasses import dataclass

@dataclass
class WeatherForecast:
    date: str
    temperature_c: int
    summary: str

    @property
    def temperature_f(self):
        return 32 + int(self.temperature_c / 0.5556)

#example
forecast = WeatherForecast(date="2023-11-02", temperature_c=20, summary="Partly cloudy")
print(f"Date: {forecast.date}")
print(f"Temperature (C): {forecast.temperature_c}")
print(f"Temperature (F): {forecast.temperature_f}")
print(f"Summary: {forecast.summary}")
