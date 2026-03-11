import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from test_data.seo_data import seo_data_url_keywords
import allure


@allure.id("10")
@allure.epic("Site")
@allure.story("SEO")
@pytest.mark.seo
@pytest.mark.parametrize("test_data", seo_data_url_keywords)
def test_check_content_keywords(test_data, class_driver, test_config):
    full_url = test_config['test_url'] + test_data["url"]
    class_driver.get(full_url)
    with allure.step("Get page body"):
        WebDriverWait(class_driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body = class_driver.find_element(By.TAG_NAME, "body")
    # assert body, f"Body is {body}"
    with allure.step("Check body not empty"):
        text_content = body.get_attribute("innerText")
        assert text_content is not None and text_content != "", f"Content not found {text_content}"
    with allure.step("Check body content for keywords"):
        # keywords = ["Weboldal", "készítés"]
        relevancia = all(k.lower() in text_content.lower() for k in test_data['keywords'])
        assert relevancia, f"All keywords {test_data['keywords']} not found in visible content by url: {full_url}"
    