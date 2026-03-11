import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import allure

@allure.epic("Site")
@allure.story("User can navigate")
class TestMenu:
    
    @allure.id("9")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.release_01
    @pytest.mark.regression
    def test_menu(self, class_driver, test_config):
        class_driver.get(test_config["test_url"])
        WebDriverWait(class_driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        menu_xpath = "//ul[contains(@class, 'nav')]//a"
        menu_links = class_driver.find_elements(By.XPATH, menu_xpath)
        # print(f'menu_links: {len(menu_links)}')
        menu_dict = {el.text: el.get_attribute('href') for el in menu_links if el.get_attribute('href') != test_config["test_url"] + '/'}
        # print(menu_dict)
        for menu_text, expected_url in menu_dict.items():
            with allure.step(f"Checking: {menu_text} -> {expected_url}"):
                try:
                    menu_links = class_driver.find_elements(By.XPATH, menu_xpath)
                    link = next((el for el in menu_links if el.get_attribute('href') == expected_url), None)
                    assert link is not None, f"Menu element not found by href {expected_url}"
                    
                    link.click()
                    WebDriverWait(class_driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    current_url = class_driver.current_url
                    assert current_url == expected_url, f"URL {current_url} Expected: {expected_url}"
                    # enshure than menu item is active class
                    menu_link = class_driver.find_element(By.XPATH, menu_xpath + "[contains(@class, 'now')]")
                    assert menu_link.get_attribute('href') == expected_url
                    
                    class_driver.back()
                    WebDriverWait(class_driver, 5).until(EC.presence_of_element_located((By.XPATH, menu_xpath)))
                except ElementClickInterceptedException:
                    print(f"Menu '{menu_text}' could not be clicked")
                    class_driver.get(test_config["test_url"])


