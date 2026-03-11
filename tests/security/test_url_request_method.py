import pytest
import requests
from test_data.urls_data import valid_urls_data
from test_data.requst_methods import request_methods
from requests.exceptions import TooManyRedirects, ConnectionError, Timeout


class TestUrlRequestMethod:
    
    @pytest.fixture
    def session(self):
        s = requests.Session()
        s.verify = False
        s.max_redirects = 3
        yield s
        s.close()
    

    @pytest.mark.critical
    @pytest.mark.parametrize("urls", valid_urls_data)
    @pytest.mark.parametrize("method", request_methods)
    def test_url_method(self, session, urls, method, test_config):
        full_url = test_config["test_url"] + urls["url"]
        print(f"Page: {urls['page']} Method: {method} Allowed: {urls['method']} Url: {full_url}")
        try:
            response = session.request(method=method, url=full_url, timeout=5)
            print("status_code: ", response.status_code)
            if method in urls["method"]:
                assert response.status_code in [200, 201, 202, 204, 401], f"Response status code: {response.status_code}"
                return
            expected_statuses = [405]
            assert response.status_code in expected_statuses, f"Response status code: {response.status_code}"
            
        except TooManyRedirects:
            return
        except ConnectionError as e:
            pytest.fail(f"Connection error for {full_url}: {e}")
        except Timeout as e:
            pytest.fail(f"Timeout for {full_url}: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error for {full_url}: {e}")