from playwright.sync_api import sync_playwright
from utils.template import template_validate_column, template_get

BASE_URL = "http://127.0.0.1:8080/api/v1/news"

valid_pin_id = "37776255-4347-6547-3fbd-0007ab4c0020"

def test_user_can_see_news_by_pin_id_with_valid_id():
    with sync_playwright() as p:

        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}/{valid_pin_id}")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "News fetched"

        # get data
        data = body["data"]
        data_fields = ["data", "total_page", "total_item", "start_item", "end_item"]
        for dt in data_fields:
            assert dt in data

        # validate pagination fields
        pagination_fields = ["total_page", "total_item", "start_item", "end_item"]
        template_validate_column([data], pagination_fields, "number", False)

        # validate data
        list_fields_str = ["news_title","news_url","news_source","published_at"]
        template_validate_column(data['data'], list_fields_str, "string", False)

        request_context.dispose()

def test_user_cant_see_news_by_pin_id_with_invalid_id():
    with sync_playwright() as p:
        pin_id = "1"

        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}/{pin_id}")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "pin_id must be valid uuid"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_see_news_by_pin_id_with_invalid_id_not_found():
    with sync_playwright() as p:
        pin_id = "37776255-4347-6547-3fbd-0007ab4cabcd"

        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}/{pin_id}")

        # default test
        body = template_get(response, 404, None)
        assert body["status"] == "failed"
        assert body["message"] == "pin_id not found"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_see_news_by_pin_id_with_invalid_page():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}/{valid_pin_id}?page=A")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "page must be a positive number"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_see_news_by_pin_id_with_invalid_per_page():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}/{valid_pin_id}?per_page=A")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "per_page must be a positive number"
        assert body["data"] == None

        request_context.dispose()