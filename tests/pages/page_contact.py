import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from test_data.send_message_data import required_inputs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class PageContact:
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self._form = None
    
    def load_page(self, full_url):
        with allure.step(f"Page url loadad: {full_url}"):
            self.driver.get(full_url)
        return self
    
    def refresh_page_state(self):
        self._form = None
        
    
    @property
    def form(self):
        if self._form is None:
            with allure.step("Get form"):
                WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.ID, "arajanlat")))
                self._form = self.driver.find_element(By.ID, "arajanlat")
        return self._form
    
    @property
    def name_input(self):
        return self._get_field("name")
    
    @property
    def email_input(self):
        return self._get_field("email")
    
    @property
    def telefon_input(self):
        return self._get_field("telefon")
    
    @property
    def kezdes_input(self):
        return self._get_field("kezdes")
    
    @property
    def honnan_select(self):
        return self._get_field("honnan")
    
    @property
    def captha_input(self):
        return self._get_field("captcha")
    
    @property
    def send_button(self):
        with allure.step("Get submit button"):
            return self.form.find_element(By.XPATH, ".//input[@id='sendbutton']")
    
    def _get_form(self):
        return self._form
    
    def _get_field(self, field_name: str):
        with allure.step(f"Get field {field_name}"):
            if not (field_data := next((el for el in required_inputs if el['name'] == field_name), None)):
                pytest.fail(f"Can't find field {field_name}. Check testing data")
            condition = ' and '.join(f"contains(@{k}, '{v}')" for k, v in field_data['find_by'].items())
            return self.form.find_element(By.XPATH, f".//*[{condition}]")
    
    def _check_field_proprs(self, field, props: dict):
        errors = []
        for prop, expected_val in props.items():
            with allure.step(f"Checking {prop} == {expected_val}"):
                try:
                    actual_val = field.get_attribute(prop)
                    
                    if isinstance(expected_val, bool):
                        # required, readonly, disabled
                        if expected_val:
                            assert actual_val is not None, f"Prop '{prop}' not found"
                        else:
                            assert actual_val is None, f"Prop '{prop}' not found"
                    elif isinstance(expected_val, int):
                        # maxlength, minlength
                        assert actual_val is not None, f"Prop '{prop}' not found"
                        assert int(actual_val) == expected_val, f"Prop '{prop}' val: {expected_val}, got {actual_val}"
                    else:
                        # type, placeholder, pattern
                        assert actual_val == expected_val, f"Prop '{prop}' val '{expected_val}', got '{actual_val}'"
                            
                except AssertionError as e:
                    errors.append(str(e))
                except Exception as e:
                    errors.append(f"Error checking '{prop}': {str(e)}")
        
        if errors:
            error_msg = "\n".join(errors)
            pytest.fail(f"Field property check failed:\n{error_msg}")
            return
            # raise AssertionError(f"Field property check failed:\n{error_msg}")
        
        print(f"✓ All properties verified: {list(props.keys())}")
    