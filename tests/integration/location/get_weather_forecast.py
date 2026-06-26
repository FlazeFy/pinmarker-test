from playwright.sync_api import sync_playwright
from utils.auth import do_login_api
from utils.template import template_validate_column, template_get
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8080/api/v1/location/forecast"

tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
after_16_days = (datetime.now() + timedelta(days=16)).strftime("%Y-%m-%d")

def test_user_can_see_weather_forecast_with_valid_param():
    with sync_playwright() as p:
        token = do_login_api(p)
        
        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?pin_id=7683af0d-831a-2885-37dc-082c565292f5&lat=-6.219728668926187&long=106.8125110497443&start_date={tomorrow}&end_date={tomorrow}")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "weather forecast fetched"

        # get data
        data = body["data"]

        assert "timezone" in data
        assert "weather" in data
        assert "air" in data

        assert isinstance(data["timezone"], str)

        # validate weather fields
        weather_fields_str = ["datetime"]
        weather_fields_number = ["temperature", "feels_like", "humidity", "wind_speed", "code"]
        template_validate_column(data["weather"], weather_fields_str, "string", False)
        template_validate_column(data["weather"], weather_fields_number, "number", False)

        # validate air fields
        air_fields_str = ["datetime"]
        air_fields_number = ["aqi", "pm2_5", "pm10", "co", "no2"]
        template_validate_column(data["air"], air_fields_str, "string", False)
        template_validate_column(data["air"], air_fields_number, "number", False)

        request_context.dispose()

def test_user_cant_see_weather_forecast_with_invalid_lat_type():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?pin_id=7683af0d-831a-2885-37dc-082c565292f5&lat=A&long=106.8125110497443&start_date={tomorrow}&end_date={tomorrow}")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "lat must be valid number"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_see_weather_forecast_with_invalid_pin_id():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?pin_id=1&lat=-6.219728668926187&long=106.8125110497443&start_date={tomorrow}&end_date={tomorrow}")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "pin_id must be valid uuid"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_see_weather_forecast_with_empty_end_date():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?pin_id=7683af0d-831a-2885-37dc-082c565292f5&lat=-6.219728668926187&long=106.8125110497443&start_date={tomorrow}")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "date is required"
        assert body["data"] == None

        request_context.dispose()

def test_user_can_see_weather_forecast_with_invalid_past_date():
    with sync_playwright() as p:
        token = do_login_api(p)
        
        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?pin_id=7683af0d-831a-2885-37dc-082c565292f5&lat=-6.219728668926187&long=106.8125110497443&start_date=1990-01-01&end_date={tomorrow}")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "start_date must be today or later"
        assert body["data"] == None

        request_context.dispose()

def test_user_can_see_weather_forecast_with_invalid_date_range():
    with sync_playwright() as p:
        token = do_login_api(p)
        
        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?pin_id=7683af0d-831a-2885-37dc-082c565292f5&lat=-6.219728668926187&long=106.8125110497443&start_date={after_16_days}&end_date={after_16_days}")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "date must be within 14 days from today"
        assert body["data"] == None

        request_context.dispose()