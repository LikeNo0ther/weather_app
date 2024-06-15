from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx

app = FastAPI()


BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "72397f7a8e86404e2944102b8162e223"

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def get_city(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/weather", response_class=HTMLResponse)
def get_weather(city: str, request: Request):
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "ru"}
    response = httpx.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_data = {
            "city": data["name"],
            "temperature": round(data["main"]["temp"]),
            "weather": data["weather"][0]["description"],
        }
        return templates.TemplateResponse(
            "weather.html",
            {"request": request, "weather_data": weather_data}
        )
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Город не найден"
        )
