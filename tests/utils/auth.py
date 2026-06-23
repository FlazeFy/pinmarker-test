from playwright.sync_api import sync_playwright
from utils.template import template_get

BASE_URL = "http://127.0.0.1:8080/api/v1/auth/login"

def do_login_api(p):
    # create request context
    request_context = p.request.new_context()
    response = request_context.post(BASE_URL, data={
        "username": "tester_user",
        "password": "admin"
    })

    body = template_get(response, 200, None)
    token = body["data"]["token"]
    request_context.dispose()

    return token

