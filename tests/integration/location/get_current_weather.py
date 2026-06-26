from playwright.sync_api import sync_playwright
from utils.auth import do_login_api
from utils.template import template_validate_column
from utils.template import template_get
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8080/api/v1/location/weather"

def test_user_can_get_current_weather_with_valid_param():
    with sync_playwright() as p:
        token = do_login_api(p)
        
        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?lat=-6.219728668926187&long=106.8125110497443")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "weather fetched"

        # get data
        data = body["data"]

        assert "weather" in data
        assert "air" in data

        # validate weather fields
        weather_fields_str = ["unit"]
        weather_fields_number = ["temperature", "feels_like", "humidity", "wind_speed", "code"]
        template_validate_column(data["weather"], weather_fields_str, "string", False)
        template_validate_column(data["weather"], weather_fields_number, "number", False)

        # validate air fields
        air_fields_number = ["aqi", "pm2_5", "pm10", "co", "no2"]
        template_validate_column(data["air"], air_fields_number, "number", False)

        request_context.dispose()

def test_user_cant_get_current_weather_with_invalid_lat_type():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?lat=A&long=106.8125110497443")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "lat must be valid number"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_get_current_weather_with_empty_coordinate():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?long=106.8125110497443")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "coordinate is required"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_get_current_weather_with_invalid_coordinate_number():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?lat=-6.219728668926187&long=206.8125110497443")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "long is invalid"
        assert body["data"] == None

        request_context.dispose()