import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class TestMenu:
    
    @pytest.mark.release_01
    # @pytest.mark.regression
    def test_menu(self, driver, test_config):
        driver.get(test_config["test_url"])
        print(driver.__dict__)
        # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        # menu_links = driver.get_elements(By.XPATH, "//ul[contains(@class, 'nav')]//a")
        # for link in menu_links:
        #     link.click()
        #     driver.url()