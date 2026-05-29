from playwright.sync_api import sync_playwright
from utils.template import template_get, template_validate_column

def test_user_can_see_nearby_places_with_valid_coordinate():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get("http://127.0.0.1:8080/api/v1/location/reverse?lat=-6.226647596739904&long=106.82214655132219")

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

def test_user_cant_see_nearby_places_with_invalid_coordinate():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get("http://127.0.0.1:8080/api/v1/location/reverse?lat=-6.226647596739904")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "coordinate is required"
        assert body["data"] == None