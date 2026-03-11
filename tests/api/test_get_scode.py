import pytest
from test_data.urls_data import valid_urls_data
import allure

@allure.epic("API")
class TestScodeAPI:
    
    @pytest.fixture
    def full_url(self, test_config):
        page_url = next((u["url"] for u in valid_urls_data if u["page"] == "get_scode"), None)
        assert page_url, "page_url not found"
        return test_config['test_url'] + page_url
    
    
    @allure.id("21")
    @pytest.mark.positive
    def test_get_scode_success(self, session, test_config, auth_headers, full_url):
        # print("auth_headers: ", auth_headers)
        with allure.step("get scode with session id"):
            resp = session.get(test_config['test_url'] + '/function/scode.php')
            session_id = session.cookies.get('PHPSESSID')
            print(f"Session ID: {session_id}")
        with allure.step("Check contet type is image/png"):
            expected_content_type = "image/png"
            content_type = resp.headers.get('content-type')
            assert expected_content_type == content_type, f"Invalid content-type: {content_type}, expected: {expected_content_type}"
        with allure.step("Send API request to get scode result"):
            response = session.get(full_url, headers=auth_headers)
            assert session_id == session.cookies.get('PHPSESSID'), "Session PHPSESSID not equal!"
            assert response.status_code == 200
            json_data = response.json()
            assert json_data['success'] is True
            print(f"\nscode: {json_data['data']}")
            scode = json_data['data']
        with allure.step("Check scode type"):
            assert isinstance(scode, int), f"Scode is {scode}, expected integer!"
            return scode
