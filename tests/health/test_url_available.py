import pytest
import requests
from test_data.urls_data import valid_urls_data
from requests.exceptions import TooManyRedirects, ConnectionError, Timeout
import allure


class TestUrlAvailable:
    
    @pytest.fixture
    def session(self):
        s = requests.Session()
        s.verify = False
        s.max_redirects = 3
        yield s
        s.close()
    
    @allure.id("13")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.run(order=0)
    @pytest.mark.smoke
    @pytest.mark.parametrize("urls", valid_urls_data)
    def test_url_availability(self, session, urls, test_config):
        full_url = test_config["test_url"] + urls["url"]
        for method in urls["method"]:
            print(f"Page: {urls['page']} Method: {method} Url: {full_url}")
            try:
                response = session.request(method=method, url=full_url, timeout=5)
                print("status_code: ", response.status_code)
                assert response.status_code in [200, 201, 202, 204, 401], f"Response status code: {response.status_code}"
                
            except TooManyRedirects as e:
                pytest.fail(f"Too many redirects for {full_url}: {e}")
            except ConnectionError as e:
                pytest.fail(f"Connection error for {full_url}: {e}")
            except Timeout as e:
                pytest.fail(f"Timeout for {full_url}: {e}")
            except Exception as e:
                pytest.fail(f"Unexpected error for {full_url}: {e}")