from playwright.sync_api import sync_playwright
from utils.template import template_validate_graphql_error, template_validate_column

BASE_URL = "http://localhost:4000/graphql"

def test_user_can_search_visit_histories_with_valid_start_and_end_date():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()

        response = request_context.post(
            BASE_URL,
            data={
                "query": """
                query {
                    visitHistories(
                        start_date: "2026-01-01"
                        end_date: "2026-07-03"
                    ) {
                        id
                        visit_desc
                        visit_by
                        visit_with
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
        data = body["data"]["visitHistories"]
        assert len(data) > 0

        # validate data
        fields_string = ["id", "visit_desc", "visit_by", "visit_with", "created_at"]
        template_validate_column(data, fields_string, "string", False)

        request_context.dispose()

def test_user_can_search_visit_histories_with_valid_start_and_end_datetime():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()

        response = request_context.post(
            BASE_URL,
            data={
                "query": """
                query {
                    visitHistories(
                        start_date: "2026-01-01T00:00:00.000Z"
                        end_date: "2026-07-03T23:59:59.999Z"
                    ) {
                        id
                        visit_desc
                        visit_by
                        visit_with
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
        data = body["data"]["visitHistories"]
        assert len(data) > 0

        # validate data
        fields_string = ["id", "visit_desc", "visit_by", "visit_with", "created_at",]
        template_validate_column(data, fields_string, "string", False)

        request_context.dispose()

def test_user_cant_search_visit_histories_with_invalid_start_date():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()

        response = request_context.post(
            BASE_URL,
            data={
                "query": """
                query {
                    visitHistories(
                        start_date: "invalid-date"
                        end_date: "2026-07-03"
                    ) {
                        id
                        visit_desc
                        visit_by
                        visit_with
                        created_at
                    }
                }
                """
            }
        )

        # default test
        assert response.status == 200
        body = response.json()
        assert "errors" in body

        # validate error
        template_validate_graphql_error(body, "start_date must be a valid date", "BAD_USER_INPUT")

        request_context.dispose()

def test_user_cant_search_visit_histories_with_empty_end_date():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()

        response = request_context.post(
            BASE_URL,
            data={
                "query": """
                query {
                    visitHistories(
                        start_date: "2026-01-01"
                        end_date: ""
                    ) {
                        id
                        visit_desc
                        visit_by
                        visit_with
                        created_at
                    }
                }
                """
            }
        )

        # default test
        assert response.status == 200
        body = response.json()
        assert "errors" in body

        # validate error
        template_validate_graphql_error(body, "start_date and end_date are required", "BAD_USER_INPUT")

        request_context.dispose()