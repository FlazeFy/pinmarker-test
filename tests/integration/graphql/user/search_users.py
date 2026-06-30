from playwright.sync_api import sync_playwright
from utils.template import template_validate_column

BASE_URL = "http://localhost:4000/graphql"

def test_user_can_search_user_with_valid_search():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()

        response = request_context.post(
            BASE_URL,
            data={
                "query": """
                query {
                    searchUsers(search: "Leo") {
                        email
                        fullname
                        img_url
                        id
                        total_pin
                        total_review
                        total_visit
                        username
                        created_at
                    }
                }
                """
            }
        )

        # default test
        assert response.status == 200
        body = response.json()
        assert "errors" not in body

        # get data
        data = body["data"]["searchUsers"]
        assert len(data) > 0

        # validate data
        fields_string = ["id", "username", "email", "fullname", "created_at"]
        fields_string_nullable = ["img_url"]
        fields_int = ["total_pin", "total_visit", "total_review"]
        template_validate_column(data, fields_string, "string", False)
        template_validate_column(data, fields_int, "number", False)
        template_validate_column(data, fields_string_nullable, "string", True)

        request_context.dispose()

def test_user_cant_search_user_with_invalid_search():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()

        response = request_context.post(
            BASE_URL,
            data={
                "query": """
                query {
                    searchUsers(search: "invalid_user") {
                        email
                        fullname
                        img_url
                        id
                        total_pin
                        total_review
                        total_visit
                        username
                        created_at
                    }
                }
                """
            }
        )

        # default test
        assert response.status == 200
        body = response.json()
        assert "errors" not in body

        # get data
        data = body["data"]["searchUsers"]
        assert data == []

        request_context.dispose()