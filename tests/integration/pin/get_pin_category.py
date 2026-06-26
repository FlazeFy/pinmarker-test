from playwright.sync_api import sync_playwright
from utils.auth import do_login_api
from utils.template import template_validate_column, template_get

BASE_URL = "http://127.0.0.1:8080/api/v1/pin"

def test_user_can_see_pin_category():
    with sync_playwright() as p:
        token = do_login_api(p)
        
        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get(f"{BASE_URL}/pin_category")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "Pin category fetched"

        # get data
        data = body["data"]

        # validate fields
        fields_str = ["pin_category","dictionary_color"]
        template_validate_column(data, fields_str, "string", False)

        fields_str_nullable = ["dictionary_icon"]
        template_validate_column(data, fields_str_nullable, "string", True)

        fields_int = ["total"]
        template_validate_column(data, fields_int, "number", False)

        request_context.dispose()