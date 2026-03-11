import pytest
from test_data.urls_data import valid_urls_data
import allure


@allure.epic("API")
class TestPartnersAPI:
        
    @pytest.fixture
    def full_url(self, test_config):
        page_url = next((u["url"] for u in valid_urls_data if u["page"] == "get_partners"), None)
        assert page_url, "page_url not found"
        return test_config['test_url'] + page_url
    
    @allure.id("14")
    @pytest.mark.positive
    def test_get_partners_positive(self, session, auth_headers, full_url):
        response = session.get(full_url, headers=auth_headers)
        assert response.status_code == 200
        json_data = response.json()
        assert json_data['success'] is True
        assert 'data' in json_data
        assert isinstance(json_data['data'], list)
        assert 'count' in json_data
        print(f"\nData lenght: {json_data['count']}")
    
    
    @allure.id("15")
    @pytest.mark.negative
    def test_get_partners_negative(self, session, full_url):
        response = session.get(full_url)
        assert response.status_code == 401
        # check with fake Token
        auth_headers = {'Authorization': 'Token 3423rsgdrydfghbfgjhfh'}
        response = session.get(full_url, headers=auth_headers)
        assert response.status_code == 401
        
