from playwright.sync_api import sync_playwright
from utils.auth import do_login_api
from utils.template import template_validate_column
from utils.template import template_get

BASE_URL = "http://127.0.0.1:8080/api/v1/schedule"

def test_user_can_see_all_schedule_with_valid_query_param():
    with sync_playwright() as p:
        token = do_login_api(p)
        
        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?search=food&pin_category=Restaurant&max_distance=5&lat=-6.2264834021121365&long=106.82247833949344&is_favorite=all&is_visited=all&open_status=all")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "Schedule fetched"

        # get data
        data = body["data"]

        # validate pin fields
        pin_fields_str = ["id", "pin_name", "schedule_day", "pin_category"]
        pin_fields_nullable_str = ["schedule_hour_start", "schedule_hour_end"]
        pin_fields_number = ["is_24_h", "is_closed", "is_favorite"]
        pin_fields_nullable_number = ["distance"]
        template_validate_column(data, pin_fields_str, "string", False)
        template_validate_column(data, pin_fields_nullable_str, "string", True)
        template_validate_column(data, pin_fields_number, "number", False)
        template_validate_column(data, pin_fields_nullable_number, "number", True)

        request_context.dispose()

def test_user_can_see_all_schedule_with_invalid_search_not_found():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?search=notfound")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "No schedule found"
        assert len(body["data"]) == 0

        request_context.dispose()

def test_user_cant_see_all_schedule_with_invalid_max_distance():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?max_distance=A")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "max_distance must be a positive number"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_see_all_schedule_with_invalid_is_visited():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?is_visited=2")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "is_visited not valid"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_see_all_schedule_with_invalid_open_status():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?open_status=2")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "open_status not valid"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_see_all_schedule_with_invalid_is_favorite():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?is_favorite=2")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "is_favorite not valid"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_see_all_schedule_with_invalid_coordinate():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?lat=-6.2264834021121365")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "coordinate not valid"
        assert body["data"] == None

        request_context.dispose()