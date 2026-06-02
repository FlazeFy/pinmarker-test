from playwright.sync_api import sync_playwright
from utils.template import template_validate_column
from utils.template import template_get

BASE_URL = "http://127.0.0.1:8080/api/v1/pin/maps"

def test_user_can_see_pin_maps_with_valid_query_param():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}?search=bebek&pin_category=Restaurant&page=1&per_page=50&max_distance=5&lat=-6.2302092800454325&long=106.81814749063726&is_favorite=all&is_visited=all")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "Pin fetched"

        # get data
        data = body["data"]
        data_fields = ["data", "total_page", "total_item", "start_item", "page", "per_page", "end_item", "visited_percentage", "average_distance"]
        for dt in data_fields:
            assert dt in data

        # validate pagination fields
        pagination_fields = ["page", "per_page", "total_page", "total_item", "start_item", "end_item", "visited_percentage", "average_distance"]
        template_validate_column([data], pagination_fields, "number", False)

        # validate pin fields
        pin_fields_str = ["id", "pin_name", "pin_address", "pin_category", "created_at"]
        pin_fields_nullable_str = ["pin_desc", "last_visit_at"]
        pin_fields_number = ["total_visit", "is_favorite", "pin_lat", "pin_long"]
        pin_fields_nullable_number = ["distance"]
        template_validate_column(data["data"], pin_fields_str, "string", False)
        template_validate_column(data["data"], pin_fields_nullable_str, "string", True)
        template_validate_column(data["data"], pin_fields_number, "number", False)
        template_validate_column(data["data"], pin_fields_nullable_number, "number", True)

        request_context.dispose()

def test_user_can_see_pin_maps_with_invalid_search_not_found():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}?search=notfound")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "No pins found"
        assert len(body["data"]["data"]) == 0

        request_context.dispose()

def test_user_cant_see_pin_maps_with_invalid_max_distance():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}?max_distance=A")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "max_distance must be a positive number"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_see_pin_maps_with_invalid_is_visited():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}?is_visited=2")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "is_visited not valid"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_see_pin_maps_with_invalid_is_favorite():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}?is_favorite=2")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "is_favorite not valid"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_see_pin_maps_with_invalid_page():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}?page=A")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "page must be a positive number"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_see_pin_maps_with_invalid_per_page():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}?per_page=A")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "per_page must be a positive number"
        assert body["data"] == None

        request_context.dispose()