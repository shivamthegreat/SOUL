import requests
from datetime import datetime

def fetch_weather(city):
    """
    Fetch current weather and 3-day forecast for a city.
    """
    api_key = "a4f1ccec457876624058d9e956ae660b"
    
    # --- Current weather ---
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    current_data = response.json()

    if str(current_data.get("cod")) == "404":
        return "Sorry, I couldn't find that city. Please try again."

    # Extract current weather data
    main = current_data["main"]
    weather_desc = current_data["weather"][0]["description"]
    icon_code = current_data["weather"][0]["icon"]
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    temp = main["temp"]
    feels_like = main["feels_like"]
    pressure = main["pressure"]
    humidity = main["humidity"]
    wind_speed = current_data["wind"]["speed"]

    sunrise_ts = current_data["sys"]["sunrise"]
    sunset_ts = current_data["sys"]["sunset"]
    sunrise_time = datetime.fromtimestamp(sunrise_ts).strftime("%H:%M")
    sunset_time = datetime.fromtimestamp(sunset_ts).strftime("%H:%M")

    # --- 3-day forecast ---
    forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
    forecast_params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "cnt": 24  # next 24 intervals (~3 days, 3-hour steps)
    }
    forecast_resp = requests.get(forecast_url, params=forecast_params)
    forecast_data = forecast_resp.json()

    if "list" not in forecast_data:
        forecast_text = "Forecast data unavailable."
    else:
        # Summarize forecast at 12:00 each day
        daily_forecasts = []
        for entry in forecast_data["list"]:
            time_txt = entry["dt_txt"]
            if "12:00:00" in time_txt:
                date_str = datetime.strptime(time_txt, "%Y-%m-%d %H:%M:%S").strftime("%A")
                desc = entry["weather"][0]["description"]
                day_temp = entry["main"]["temp"]
                daily_forecasts.append(f"{date_str}: {desc}, {day_temp}°C")
        forecast_text = "\n".join(daily_forecasts)

    # --- Compose final response ---
    final_response = (
        f"Current weather in {city}:\n"
        f"- {weather_desc.capitalize()} ({icon_url})\n"
        f"- Temperature: {temp}°C (feels like {feels_like}°C)\n"
        f"- Pressure: {pressure} hPa\n"
        f"- Humidity: {humidity}%\n"
        f"- Wind speed: {wind_speed} km/h\n"
        f"- Sunrise at {sunrise_time}, sunset at {sunset_time}\n\n"
        f"Upcoming forecast:\n{forecast_text}"
    )
    return final_response
