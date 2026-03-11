import pytest
import requests
from test_data.login_data import valid_login_data, invalid_login_data
from test_data.urls_data import valid_urls_data
import allure


@allure.epic("API")
@allure.feature("User can login")
class TestLoginAPI:
    
    @pytest.fixture
    def session(self):
        s = requests.Session()
        print(f"New session - {id(s)}")
        s.verify = False
        yield s
        s.close()
        
    @pytest.fixture
    def full_url(self, test_config):
        page_url = next((u["url"] for u in valid_urls_data if u["page"] == "login"), None)
        assert page_url, "page_url not found"
        return test_config['test_url'] + page_url
    
    @allure.id("16")
    @pytest.mark.positive
    @pytest.mark.security
    def test_login_success(self, session, full_url):
        response = session.post(full_url, data=valid_login_data)
        assert response.status_code == 200
        json_data = response.json()
        assert json_data['success'] is True
        assert 'token' in json_data
        assert json_data['token'] != ""
        assert 'user' in json_data
        assert json_data['user']['username'] == valid_login_data["username"]
    
    @allure.id("17")
    @pytest.mark.negative
    @pytest.mark.security
    @pytest.mark.parametrize("invalid_login_data", invalid_login_data)
    def test_login_invalid_credentials(self, invalid_login_data, session, full_url):
        response = session.post(full_url, data=invalid_login_data)
        assert response.status_code == 401
        json_data = response.json()
        assert 'error' in json_data
        assert 'success' not in json_data or json_data.get('success') is False

    @allure.id("20")
    @pytest.mark.negative
    @pytest.mark.security
    def test_login_content_type(self, session, full_url):
        import json
        headers = {'Content-Type': 'application/json'}        
        response = session.post(full_url, data=json.dumps(valid_login_data), headers=headers)
        assert response.status_code == 401
    