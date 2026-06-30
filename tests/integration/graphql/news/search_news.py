from playwright.sync_api import sync_playwright
from utils.template import template_validate_column

BASE_URL = "http://localhost:4000/graphql"

def test_user_can_search_news_with_valid_params():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()

        response = request_context.post(
            BASE_URL,
            data={
                "query": """
                query {
                    searchNews(news_title: "cafe", pin_name: "cafe") {
                        created_at
                        id
                        news_source
                        news_title
                        news_url
                        pin_address
                        pin_category
                        pin_city
                        pin_country
                        pin_id
                        pin_lat
                        pin_long
                        pin_name
                        pin_suburb
                        pin_village
                        published_at
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
        data = body["data"]["searchNews"]
        assert len(data) > 0

        # validate data
        fields_string = ["id", "news_source", "news_title", "news_url", "pin_country", "pin_category", "pin_id", "pin_lat", "pin_long", "pin_name", "created_at"]
        fields_string_nullable = ["pin_address", "pin_city", "pin_suburb", "pin_village"]
        template_validate_column(data, fields_string, "string", False)
        template_validate_column(data, fields_string_nullable, "string", True)

        request_context.dispose()

def test_user_cant_search_news_with_invalid_not_found_news_title():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()

        response = request_context.post(
            BASE_URL,
            data={
                "query": """
                query {
                    searchNews(news_title: "invalid news") {
                        created_at
                        id
                        news_source
                        news_title
                        news_url
                        pin_address
                        pin_category
                        pin_city
                        pin_country
                        pin_id
                        pin_lat
                        pin_long
                        pin_name
                        pin_suburb
                        pin_village
                        published_at
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
        data = body["data"]["searchNews"]
        assert data == []

        request_context.dispose()