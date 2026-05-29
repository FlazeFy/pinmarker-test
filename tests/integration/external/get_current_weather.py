from playwright.sync_api import sync_playwright
from utils.template import template_get, template_validate_column

def test_user_can_see_current_weather_with_valid_coordinate():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get("http://127.0.0.1:8080/api/v1/location/weather?lat=-6.226647596739904&long=106.82214655132219")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "weather fetched"

        # get data
        data = body["data"]
        assert "weather" in data
        assert "air" in data

        # validate weather fields
        weather_fields = ["temperature", "feels_like", "humidity", "wind_speed", "code"]
        template_validate_column(data["weather"], weather_fields, "number", False)
        assert isinstance(data["weather"]["unit"], str)

        # validate air fields
        air_fields = ["aqi", "pm2_5", "pm10", "co", "no2"]
        template_validate_column(data["air"], air_fields, "number", False)

        request_context.dispose()

def test_user_cant_see_current_weather_with_invalid_coordinate():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get("http://127.0.0.1:8080/api/v1/location/weather?lat=-6.226647596739904")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "coordinate is required"
        assert body["data"] == None