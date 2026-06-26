from playwright.sync_api import sync_playwright
from utils.auth import do_login_api
from utils.template import template_validate_column, template_get

BASE_URL = "http://127.0.0.1:8080/api/v1/pin/search"

def test_user_can_see_all_pin_search_format_with_valid_query_param():
    with sync_playwright() as p:
        token = do_login_api(p)
        
        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?search=Matcha")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "Pin fetched"

        # get data
        data = body["data"]

        # validate pin fields
        pin_fields_str = ["id", "pin_name", "pin_final_address", "pin_category"]
        pin_fields_nullable_str = ["pin_image"]
        pin_fields_number = ["is_favorite", "pin_lat", "pin_long"]
        template_validate_column(data, pin_fields_str, "string", False)
        template_validate_column(data, pin_fields_nullable_str, "string", True)
        template_validate_column(data, pin_fields_number, "number", False)

        request_context.dispose()

def test_user_can_see_all_pin_search_format_with_invalid_search_not_found():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?search=notfound")

        # default test
        body = template_get(response, 404, None)
        assert body["status"] == "failed"
        assert body["message"] == "No pin found"
        assert len(body["data"]) == 0

        request_context.dispose()

def test_user_cant_see_all_pin_search_format_with_invalid_page():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}?search=LoremipsumdolorsitametconsecteturadipiscingelitSeddoeiusmodtemporincididuntutlaboreetdoloremagnaaliquaUtenimadminimveniamquisUtenimadminimveniamq")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "search must be less than 144 characters"
        assert body["data"] == None

        request_context.dispose()
