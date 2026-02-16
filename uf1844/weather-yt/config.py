USE_ROUNDED_COORDS = True
PREFERRED_METHOD = "auto"
OPENWEATHER_API = "7549b3ff11a7b2f3cd25b56d21c83c6a"
OPENWEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather?"
    "lat={latitude}&lon={longitude}&"
    "appid=" + OPENWEATHER_API + "&lang=ru&"
    "units=metric"
)

# https://api.openweathermap.org/data/2.5/weather?lat=37.38283&lon=-5.97317&appid=7549b3ff11a7b2f3cd25b56d21c83c6a&lang=ru&units=metric