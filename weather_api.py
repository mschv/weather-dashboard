import requests
from datetime import date
import pandas as pd

def get_coordinates(city):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    params={"name":city,"count":1,"language":"en","format":"json"}
    response=requests.get(geo_url,params=params).json()

    if "results" not in response:
        return None
    
    result=response["results"][0]
    return{
        "latitude":result["latitude"],
        "longitude":result["longitude"],
        "name":result["name"],
        "country":result["country"]
    }

def get_weather(city):
    location=get_coordinates(city)
    if not location:
        return{"error":"City not found"}
    
    weather_url="https://api.open-meteo.com/v1/forecast"
    params={
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "current_weather": True
    }

    response=requests.get(weather_url,params=params).json()

    if "current_weather" not in response:
        return{"error":"No weather data available"}
    
    weather=response["current_weather"]
    return{
        "city": location["name"],
        "country": location["country"],
        "temperature": weather["temperature"],
        "windspeed": weather["windspeed"],
        "weathercode": weather["weathercode"],
        "icon": get_weather_icon(weather["weathercode"])
    }

def get_historical_weather(city, start_date,end_date):
    location=get_coordinates(city)
    if not location:
        return {"error":"City not found"}
    
    url = "https://archive-api.open-meteo.com/v1/archive"
    params={
        "latitude":location["latitude"],
        "longitude": location["longitude"],
        "start_date": start_date,
        "end_date": end_date,
        "daily": ["temperature_2m_max", "temperature_2m_min"],
        "timezone": "auto"
    }

    response=requests.get(url,params=params).json()

    if "daily" not in response:
        return {"error":"No historical data found"}
    
    df=pd.DataFrame(response["daily"])
    df["date"]=pd.to_datetime(df["time"])
    df["city"]=location["name"]
    return df

def get_weather_icon(code):
    icons = {
        0: "☀️",   # Clear sky
        1: "🌤️",  # Mainly clear
        2: "⛅",   # Partly cloudy
        3: "☁️",   # Overcast
        45: "🌫️",  # Fog
        48: "🌫️",  # Depositing rime fog
        51: "🌦️",  # Drizzle: Light
        61: "🌧️",  # Rain: Slight
        71: "🌨️",  # Snow fall: Slight
        80: "🌧️",  # Rain showers: Slight
        95: "⛈️",  # Thunderstorm
        99: "🌩️",  # Thunderstorm with hail
    }
    return icons.get(code, "❓")