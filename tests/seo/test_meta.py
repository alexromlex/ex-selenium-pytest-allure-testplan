import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from test_data.seo_data import seo_meta_data, seo_link_data, seo_data_url_keywords
import allure

@allure.id("12")
@allure.testcase("12")
@allure.epic("Site")
@allure.story("SEO")
@pytest.mark.seo
@pytest.mark.parametrize("seo_data", seo_data_url_keywords)
def test_meta(seo_data, class_driver, test_config):
    full_url = test_config['test_url'] + seo_data['url']
    allure.dynamic.title(f"Test url: {full_url}")
    class_driver.get(full_url)
    with allure.step("Get page head"):
        WebDriverWait(class_driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, "head")))
        head = class_driver.find_element(By.TAG_NAME, "head")
    all_test_data = [
        {"title": "meta", "data": seo_meta_data},
        {"title": "link", "data": seo_link_data}
    ]
    errors = []
    for el in all_test_data:
        with allure.step(f"Verify <{el['title']}> in head"):
            for data_el in el['data']:
                with allure.step(f"Expect {data_el['name']}"):
                    condition = ' and '.join(f"contains(@{k}, '{v}')" for k, v in data_el['find_by'].items())
                    try:
                        head.find_element(By.XPATH, f".//*[{condition}]")
                    except NoSuchElementException:
                        errors.append(f"{el['title']}: {data_el['name']}: Not found with conditions: {data_el['find_by']}")
                        allure.attach(
                            f"Not found with conditions: {data_el['find_by']}",
                            name="Error",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        continue
    
    if errors:
        error_summary = "\n".join(errors)
        pytest.fail(f"Missing {len(errors)} elements:\n{error_summary}")