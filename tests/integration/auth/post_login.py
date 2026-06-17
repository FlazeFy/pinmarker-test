from playwright.sync_api import sync_playwright
from utils.template import template_validate_column
from utils.template import template_get

BASE_URL = "http://127.0.0.1:8080/api/v1/auth/login"

def test_user_can_login_with_valid_credential():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.post(BASE_URL, data={
            "username": "tester_user",
            "password": "admin"
        })

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "Login success"

        # validate data fields
        data = body["data"]
        list_fields_str = ["token", "user_id"]
        list_fields_nullable_str = ["img_url"]
        list_fields_number = ["role"]
        template_validate_column([data], list_fields_str, "string", False)
        template_validate_column([data], list_fields_nullable_str , "string", True)
        template_validate_column([data], list_fields_number, "number", False)

        # validate token is not empty
        assert data["token"] is not None
        assert len(data["token"]) > 0        

        request_context.dispose()

def test_user_cant_login_with_wrong_password():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.post(BASE_URL, data={
            "username": "tester_user",
            "password": "wrongpassword"
        })

        # default test
        body = template_get(response, 401, None)
        assert body["status"] == "failed"
        assert body["message"] == "wrong username or password"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_login_with_empty_field():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.post(BASE_URL, data={
            "username": "tester_user"
        })

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "username and password are required"
        assert body["data"] == None

        request_context.dispose()