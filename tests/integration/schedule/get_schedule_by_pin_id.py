from playwright.sync_api import sync_playwright
from utils.auth import do_login_api
from utils.template import template_validate_column
from utils.template import template_get

BASE_URL = "http://127.0.0.1:8080/api/v1/schedule"

def test_user_can_see_schedule_by_pin_id_with_valid_query_param():
    with sync_playwright() as p:
        token = do_login_api(p)
        pin_id = "38f87f06-5957-88d0-312f-6ef1b46852aa"
        
        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}/{pin_id}")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "Schedule fetched"

        # get data
        data = body["data"]

        # validate pin fields
        pin_fields_str = ["schedule_day"]
        pin_fields_nullable_str = ["schedule_hour_start", "schedule_hour_end"]
        pin_fields_number = ["is_24_h", "is_closed"]
        template_validate_column(data, pin_fields_str, "string", False)
        template_validate_column(data, pin_fields_nullable_str, "string", True)
        template_validate_column(data, pin_fields_number, "number", False)

        request_context.dispose()

def test_user_cant_see_schedule_by_pin_id_with_invalid_pin_id_not_found():
    with sync_playwright() as p:
        token = do_login_api(p)
        pin_id = "38f87f06-5957-88d0-312f-aaaaaaaaaaaa"

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}/{pin_id}")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "No schedule found"
        assert len(body["data"]) == 0

        request_context.dispose()

def test_user_cant_see_schedule_by_pin_id_with_invalid_uuid():
    with sync_playwright() as p:
        token = do_login_api(p)
        pin_id = "1"

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}/{pin_id}")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "pin_id must be valid uuid"
        assert body["data"] == None

        request_context.dispose()