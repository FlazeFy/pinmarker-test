from playwright.sync_api import sync_playwright
from utils.template import template_validate_column
from utils.template import template_get

BASE_URL = "http://127.0.0.1:8080/api/v1/global_list/recommended/tag_address"

def test_user_can_see_recommended_tag_address_with_valid_query_param():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}?limit_tag=5")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "Global list fetched"

        # get data
        data = body["data"]

        # validate data
        list_pin_address_fields_str = ["pin_address"]
        template_validate_column(data["pin_address"], list_pin_address_fields_str, "string", False)

        list_tags_fields_str = ["tag_name"]
        template_validate_column(data["tags"], list_tags_fields_str, "string", False)

        request_context.dispose()

def test_user_cant_see_recommended_tag_address_with_invalid_limit():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}?limit_tag=A")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "limit_tag must be a positive number"
        assert body["data"] == None

        request_context.dispose()