from playwright.sync_api import sync_playwright
from utils.template import template_validate_column
from utils.template import template_get

BASE_URL = "http://127.0.0.1:8080/api/v1/pin"

def test_user_can_see_pin_with_valid_query_param():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}?page=1&per_page=14&sorting=created_at-desc&pin_category=Restaurant&with_companion=1&visit_with=manuel")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "Pin fetched"

        # get data
        data = body["data"]
        data_fields = ["data", "total_page", "total_item", "start_item", "end_item", "category", "visit_with"]
        for dt in data_fields:
            assert dt in data

        # validate pagination fields
        pagination_fields = ["page", "per_page", "total_page", "total_item", "start_item", "end_item"]
        template_validate_column([data], pagination_fields, "number", False)

        # validate pin fields
        pin_fields_str = ["id", "pin_name", "pin_lat", "pin_long", "pin_address", "pin_category", "is_favorite", "created_at"]
        pin_fields_nullable_str = ["pin_desc", "pin_person", "last_visit", "visit_with"]
        pin_fields_number = ["total_visit"]
        template_validate_column(data["data"], pin_fields_str, "string", False)
        template_validate_column(data["data"], pin_fields_nullable_str, "string", True)
        template_validate_column(data["data"], pin_fields_number, "number", False)

        # validate category fields
        category_fields_str = ["pin_category"]
        category_fields_number = ["total"]
        template_validate_column(data["category"], category_fields_str, "string", False)
        template_validate_column(data["category"], category_fields_number, "number", False)

        # validate companion fields
        companion_fields_str = ["name"]
        companion_fields_number = ["total"]
        template_validate_column(data["visit_with"], companion_fields_str, "string", False)
        template_validate_column(data["visit_with"], companion_fields_number, "number", False)

        request_context.dispose()

def test_user_cant_see_pin_with_invalid_sorting_target():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}?sorting=deleted_at-asc")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "sorting not valid"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_see_pin_with_invalid_sorting_type():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}?sorting=created_at-lowest")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "sorting not valid"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_see_pin_with_invalid_companion():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}?with_companion=2")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "with_companion not valid"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_see_pin_with_invalid_page():
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

def test_user_cant_see_pin_with_invalid_per_page():
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