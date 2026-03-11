import pytest

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
import allure
from test_data.urls_data import valid_urls_data

layout_urls = [el for el in valid_urls_data if "GET" in el["method"] and "api/" not in el['url']]

@allure.epic("Site")
@allure.feature('Page Layout')
class TestPageLayout:
    
    # @pytest.mark.release_01
    @allure.id("22")
    @allure.testcase("22")
    @allure.description('Verify lang property exists on page')
    @pytest.mark.smoke
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("urls", layout_urls)
    def test_page_layout(self, test_config, function_driver: WebDriver, urls):
        allure.dynamic.title(f'Test page layout for {urls["url"]}')
        full_url = test_config['test_url'] + urls['url']
        
        with allure.step(f"Open url: {full_url}"):
            function_driver.get(full_url)
        with allure.step('Wait for body element'):
            WebDriverWait(function_driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body = function_driver.find_element(By.TAG_NAME, "body")
        with allure.step('Check body for special property: lang'):
            assert body.get_property("lang"), "Expected lang property not found"