from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import TypeAlias

from coordinates import Coordinates


Celsius: TypeAlias = int


class WeatherType(Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморось"
    RAIN = "Дождь"
    SNOW = "Снег"
    CLEAR = "Ясно"
    FOG = "Туман"
    CLOUDS = "Облачно"


@dataclass(slots=True, frozen=True)
class Weather:
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str


def get_weather(coordinates: Coordinates):
    """Request weather in OpenWeather API and returns it"""
    pass


print(WeatherType.CLEAR)
print(WeatherType.CLEAR.value)
print(WeatherType.CLEAR.name)