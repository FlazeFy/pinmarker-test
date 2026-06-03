from playwright.sync_api import sync_playwright
from utils.template import template_validate_column
from utils.template import template_get

BASE_URL = "http://127.0.0.1:8080/api/v1/visit/visit_with/analyze/Manuel"

def test_user_can_see_person_analyze_with_valid_query_param():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}?page_visit_history=1&per_page_visit_history=10")

        # default test
        body = template_get(response, 200, None)
        assert body["status"] == "success"
        assert body["message"] == "Visit companion fetched"

        # get data
        data = body["data"]

        # validate root object
        root_fields = ["visit_pertime_hour", "visit_pertime_year", "visit_pertime_dayname", "visit_location", "visit_location_category", "visit_location_favorite", "visit_daily_hour_by_person", "visit_person_summary", "visit_trends", "visit_by_person"]

        for dt in root_fields:
            assert dt in data

        # validate visit_person_summary
        visit_person_summary = data["visit_person_summary"]
        summary_fields_str = ["last_trip", "first_trip", "most_visited_category", "favorite_hour_context"]
        summary_fields_number = ["total_trip", "favorite_hour_total", "favorite_hour_context"]
        template_validate_column([visit_person_summary], summary_fields_str, "string", True)
        template_validate_column([visit_person_summary], summary_fields_number, "number", True)

        # validate visit_pertime_hour
        visit_pertime_hour = data["visit_pertime_hour"]
        visit_history_fields_str = ["visit_list"]
        visit_history_fields_number = ["context", "total"]
        template_validate_column(visit_pertime_hour, visit_history_fields_str, "string", False)
        template_validate_column(visit_pertime_hour, visit_history_fields_number, "number", False)

        # validate visit_by_person
        visit_by_person = data["visit_by_person"]
        visit_by_person_fields_str = ["id", "pin_category", "pin_address", "visit_with", "visit_at", "pin_name"]
        visit_by_person_fields_number = ["is_favorite"]
        template_validate_column(visit_by_person["data"], visit_by_person_fields_str, "string", False)
        template_validate_column(visit_by_person["data"], visit_by_person_fields_number, "number", False)

        # validate visit_daily_hour_by_person
        visit_daily_hour_by_person = data["visit_daily_hour_by_person"]
        visit_daily_hour_by_person_fields_str = ["hour", "day"]
        visit_daily_hour_by_person_fields_number = ["total"]
        template_validate_column(visit_daily_hour_by_person, visit_daily_hour_by_person_fields_str, "string", False)
        template_validate_column(visit_daily_hour_by_person, visit_daily_hour_by_person_fields_number, "number", False)

        # validate visit_location_favorite and visit_location_category
        visit_location_favorite = data["visit_location_favorite"]
        visit_location_category = data["visit_location_category"]
        visit_pertime_year = data["visit_pertime_year"]
        visit_location_favorite_fields_str = ["context"]
        visit_location_favorite_fields_number = ["total"]
        template_validate_column(visit_location_favorite, visit_location_favorite_fields_str, "string", False)
        template_validate_column(visit_location_favorite, visit_location_favorite_fields_number, "number", False)
        template_validate_column(visit_location_category, visit_location_favorite_fields_str, "string", False)
        template_validate_column(visit_location_category, visit_location_favorite_fields_number, "number", False)
        template_validate_column(visit_pertime_year, visit_location_favorite_fields_number, "number", False)

        # validate visit_location
        visit_location = data["visit_location"]
        visit_location_fields_str = ["id", "pin_category", "visit_with", "last_visit_at", "pin_name"]
        visit_location_fields_number = ["total_visit", "pin_lat", "pin_long"]
        template_validate_column(visit_location, visit_location_fields_str, "string", False)
        template_validate_column(visit_location, visit_location_fields_number, "number", False)
        
        visit_pertime_dayname = data["visit_pertime_dayname"]
        visit_pertime_dayname_fields_str = ["context", "visit_list"]
        visit_pertime_dayname_fields_number = ["total"]
        template_validate_column(visit_pertime_dayname, visit_pertime_dayname_fields_str, "string", False)
        template_validate_column(visit_pertime_dayname, visit_pertime_dayname_fields_number, "number", False)

        request_context.dispose()

def test_user_cant_see_person_analyze_with_invalid_page_visit_history():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}?page_visit_history=A")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "page_visit_history must be a positive number"
        assert body["data"] == None

        request_context.dispose()

def test_user_cant_see_person_analyze_with_invalid_per_page_visit_history():
    with sync_playwright() as p:
        # create request context
        request_context = p.request.new_context()
        response = request_context.get(f"{BASE_URL}?per_page_visit_history=A")

        # default test
        body = template_get(response, 400, None)
        assert body["status"] == "failed"
        assert body["message"] == "per_page_visit_history must be a positive number"
        assert body["data"] == None

        request_context.dispose()