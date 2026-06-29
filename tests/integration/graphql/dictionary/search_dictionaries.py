from playwright.sync_api import sync_playwright
from utils.template import template_validate_column

BASE_URL = "http://localhost:4000/graphql"

def test_user_can_search_dictionary_with_valid_dictionary_type():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()

        response = request_context.post(
            BASE_URL,
            data={
                "query": """
                query {
                    searchDictionaries(dictionary_type: "visit_by") {
                        id
                        dictionary_color
                        dictionary_icon
                        dictionary_name
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
        data = body["data"]["searchDictionaries"]
        assert len(data) > 0

        # validate data
        template_validate_column(data, ["id", "dictionary_name"], "string", False)
        template_validate_column(data, ["dictionary_color", "dictionary_icon"], "string", True)

        request_context.dispose()

def test_user_cant_search_dictionary_with_invalid_dictionary_type():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()

        response = request_context.post(
            BASE_URL,
            data={
                "query": """
                query {
                    searchDictionaries(dictionary_type: "invalid_type") {
                        id
                        dictionary_color
                        dictionary_icon
                        dictionary_name
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
        data = body["data"]["searchDictionaries"]
        assert data == []

        request_context.dispose()