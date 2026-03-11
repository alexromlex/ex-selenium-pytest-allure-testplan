import pytest
import time
import allure
from test_data.urls_data import valid_urls_data
from selenium.webdriver.common.by import By

check_urls = [el for el in valid_urls_data if "GET" in el["method"] and "api/" not in el['url']]

@allure.epic("Site")
@allure.id("23")
@allure.story("Page loading performance")
@pytest.mark.parametrize("page", check_urls)
def test_response_time(page, function_driver, test_config):
    full_url = test_config['test_url'] + page['url']
    allure.dynamic.title(f"Checking url: {full_url}")
    with allure.step("Sending request"):
        start_time = time.time()
        function_driver.get(full_url)
    with allure.step("Find body"):
        function_driver.find_element(By.TAG_NAME, 'body')
    load_time = time.time() - start_time
    print(f"Page load time: {load_time:.2f} sec")
    with allure.step("Check load time"):
        assert load_time < 10, f"Expected < 10 sec, got: {load_time:.2f} sec"
    