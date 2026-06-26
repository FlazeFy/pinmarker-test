from playwright.sync_api import sync_playwright
from utils.auth import do_login_api
from utils.template import template_get, template_validate_column

def test_user_can_see_news_around_me_with_valid_coordinate():
    with sync_playwright() as p:
        token = do_login_api(p)
        
        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get("http://127.0.0.1:8080/api/v1/news/by/coordinate?lat=-6.226647596739904&long=106.82214655132219")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "news fetched"

        # get data
        data = body["data"]
        assert "detail" in data
        assert "news" in data

        # validate detail fields
        detail_str_fields = ["address", "city", "country"]
        template_validate_column([data["detail"]], detail_str_fields, "string", False)

        detail_nullable_str_fields = ["village", "suburb"]
        template_validate_column([data["detail"]], detail_nullable_str_fields, "string", True)

        # validate air fields
        news_fields_str = ["title", "url", "published_at", "source"]
        template_validate_column(data["news"], news_fields_str, "string", False)

        request_context.dispose()

def test_user_cant_see_news_around_me_with_invalid_coordinate():
    with sync_playwright() as p:
        token = do_login_api(p)

        # create request context
        request_context = p.request.new_context(extra_http_headers={ "Authorization": f"Bearer {token}" })
        response = request_context.get("http://127.0.0.1:8080/api/v1/news/by/coordinate?lat=-6.226647596739904")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "coordinate is required"
        assert body["data"] == None