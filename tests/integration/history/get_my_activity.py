from playwright.sync_api import sync_playwright
from utils.template import template_validate_column
from utils.template import template_get

BASE_URL = "http://127.0.0.1:8080/api/v1/history"

def test_user_can_see_my_activity_with_valid_query_param():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}?page=1&per_page=14")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "History fetched"

        # get data
        data = body["data"]

        # validate data
        list_fields_str = ["id", "history_type", "history_context", "created_at"]
        template_validate_column(data["data"], list_fields_str, "string", False)

        request_context.dispose()

def test_user_cant_see_my_activity_with_invalid_page():
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

def test_user_cant_see_my_activity_with_invalid_per_page():
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