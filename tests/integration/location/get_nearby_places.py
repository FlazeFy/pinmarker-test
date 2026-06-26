from playwright.sync_api import sync_playwright
from utils.auth import do_login_api
from utils.template import template_get, template_validate_column

BASE_URL = "http://127.0.0.1:8080/api/v1/location/reverse"

def test_user_can_see_nearby_places_with_valid_coordinate():
    with sync_playwright() as p:
        token = do_login_api(p)
        
        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?lat=-6.226647596739904&long=106.82214655132219")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "reverse location fetched"

        # get data
        data = body["data"]
        assert "detail" in data
        assert "nearby" in data

        # validate detail fields
        detail_fields = ["address", "city", "country"]
        template_validate_column([data["detail"]], detail_fields, "string", False)

        # validate air fields
        nearby_fields_str = ["name", "amenity"]
        nearby_fields_number = ["lat", "lng", "distance"]
        template_validate_column(data["nearby"], nearby_fields_str, "string", False)
        template_validate_column(data["nearby"], nearby_fields_number, "number", False)

        request_context.dispose()


def test_user_cant_see_nearby_places_with_invalid_lat_type():
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

def test_user_cant_see_nearby_places_with_empty_coordinate():
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

def test_user_cant_see_nearby_places_with_invalid_coordinate_number():
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