import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from test_data.seo_data import seo_data_url_keywords
import allure

@allure.id("11")
@allure.epic("Site")
@allure.story("SEO")
@pytest.mark.seo
@pytest.mark.parametrize("test_data", seo_data_url_keywords)
def test_title(test_data, class_driver, test_config):
    class_driver.get(test_config['test_url'] + test_data["url"])
    with allure.step("Get page title"):
        WebDriverWait(class_driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "title")))
        page_title = class_driver.title
    with allure.step("Check title lenght"):
        expected_min_title_lenght = 30
        assert expected_min_title_lenght <= len(page_title), \
            f"Page title to short! Expected:{expected_min_title_lenght}, got: {len(page_title)}"
    with allure.step("Count keywords in title"):
        keywords_found = sum(1 for k in test_data["keywords"] if k.lower() in page_title.lower())
        assert test_data["keyword_title_min_len"] <= keywords_found, \
            f"Expected keywords: {test_data['keyword_title_min_len']}, got: {keywords_found}"

    