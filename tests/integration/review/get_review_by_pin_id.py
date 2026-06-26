from playwright.sync_api import sync_playwright
from utils.auth import do_login_api
from utils.template import template_validate_column, template_get

BASE_URL = "http://127.0.0.1:8080/api/v1/review"
page = 1
per_page = 14
pin_id = "bc04545e-a6d3-a4a8-3a59-439b9e2d8d63"

def test_user_can_see_review_with_valid_pin_id_and_query_param():
    with sync_playwright() as p:
        token = do_login_api(p)
        
        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}/{pin_id}?page={page}&per_page={per_page}")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "Review fetched"

        # get data
        data = body["data"]
        data_fields = ["data", "total_page", "total_item", "start_item", "end_item"]
        for dt in data_fields:
            assert dt in data

        # validate pagination fields
        pagination_fields = ["total_page", "total_item", "start_item", "end_item"]
        template_validate_column([data], pagination_fields, "number", False)

        # validate global list fields
        list_fields_str = ["review_person", "created_at"]
        list_fields_nullable_str = ["review_body"]
        list_fields_number = ["review_rate"]
        template_validate_column(data["data"], list_fields_str, "string", False)
        template_validate_column(data["data"], list_fields_nullable_str , "string", True)
        template_validate_column(data["data"], list_fields_number, "number", False)

        request_context.dispose()

def test_user_cant_see_review_with_invalid_pin_id_data_type():
    with sync_playwright() as p:
        token = do_login_api(p)
        
        pin_id = "A"

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}/{pin_id}")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "pin_id must be valid uuid"
        assert body["data"] == None

        request_context.dispose()

def test_user_can_see_review_with_invalid_pin_id_not_found():
    with sync_playwright() as p:
        token = do_login_api(p)

        pin_id = "11111111-1111-1111-1111-111111111111"

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}/{pin_id}")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "No review found"
        assert len(body["data"]["data"]) == 0

        request_context.dispose()

def test_user_cant_see_review_with_invalid_page():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}/{pin_id}?page=A")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "page must be a positive number"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_see_review_with_invalid_per_page():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}/{pin_id}?per_page=A")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "per_page must be a positive number"
        assert body["data"] == None

        request_context.dispose()