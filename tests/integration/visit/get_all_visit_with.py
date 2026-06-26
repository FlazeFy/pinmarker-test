from playwright.sync_api import sync_playwright
from utils.auth import do_login_api
from utils.template import template_validate_column, template_get

BASE_URL = "http://127.0.0.1:8080/api/v1/visit/visit_with"

def test_user_can_see_all_visit_with_with_valid_query_param():
    with sync_playwright() as p:
        token = do_login_api(p)
        
        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?page=1&per_page=14&search=A")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "Visit companion fetched"

        # get data
        data = body["data"]
        data_fields = ["data", "total_page", "total_item", "start_item", "page", "per_page", "end_item"]
        for dt in data_fields:
            assert dt in data

        # validate pagination fields
        pagination_fields = ["page", "per_page", "total_page", "total_item", "start_item", "end_item"]
        template_validate_column([data], pagination_fields, "number", False)

        # validate data
        list_fields_str = ["name", "last_visit_at"]
        template_validate_column(data["data"], list_fields_str, "string", False)
        list_fields_number = ["total_visit_with"]
        template_validate_column(data["data"], list_fields_number, "number", False)

        request_context.dispose()

def test_user_can_see_all_visit_with_with_invalid_search_not_found():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?search=notfound")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "No visit companion found"
        assert len(body["data"]["data"]) == 0

        request_context.dispose()

def test_user_cant_see_all_visit_with_with_invalid_page():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?page=A")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "page must be a positive number"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_see_all_visit_with_with_invalid_per_page():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?per_page=A")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "per_page must be a positive number"
        assert body["data"] == None

        request_context.dispose()