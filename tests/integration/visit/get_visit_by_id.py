from playwright.sync_api import sync_playwright
from utils.auth import do_login_api
from utils.template import template_validate_column, template_get

BASE_URL = "http://127.0.0.1:8080/api/v1/visit/by_id"

def test_user_can_see_visit_by_id_with_valid_id_and_query_param():
    with sync_playwright() as p:
        token = do_login_api(p)
        
        id = "2794c9c7-6232-15d6-0046-33294bca8675"

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}/{id}")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "Visit fetched"

        # get data
        data = body["data"]

        # validate global list fields
        list_fields_str = ["pin_id", "pin_name", "pin_category", "id", "visit_by", "created_at", "pin_final_address"]
        list_fields_int = ["is_favorite", "pin_lat", "pin_long"]
        list_fields_nullable_str = ["visit_desc", "visit_with", "pin_image", "updated_at"]
        template_validate_column(data, list_fields_str, "string", False)
        template_validate_column(data, list_fields_int, "integer", False)
        template_validate_column(data, list_fields_nullable_str , "string", True)

        request_context.dispose()

def test_user_cant_see_visit_by_id_with_invalid_id_data_type():
    with sync_playwright() as p:
        token = do_login_api(p)

        id = "A"

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}/{id}")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "id must be valid uuid"
        assert body["data"] == None

        request_context.dispose()

def test_user_can_see_visit_by_id_with_invalid_id_not_found():
    with sync_playwright() as p:
        token = do_login_api(p)

        id = "11111111-1111-1111-1111-111111111111"

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}/{id}")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "No visit found"
        assert body["data"] == None

        request_context.dispose()