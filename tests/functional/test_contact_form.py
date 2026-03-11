import pytest
from test_data.urls_data import valid_urls_data
from test_data.send_message_data import required_inputs, random_values, minimal_values, maximum_values, out_maximum_values
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import time
import allure
from pages.page_contact import PageContact

@allure.epic("User")
@allure.story('User can send message')
class TestContactFormFunc:

    def _fill_form_valid_data(self, fields_data: list, contact_page: PageContact):
        print("Form filling with valid data: ")
        for field in fields_data:
            if field["type"] == "input":
                try:
                    input = contact_page._get_field(field["name"])
                    input.clear()
                    input.send_keys(field["value"])
                    print(f"{field['name']}: {input.get_attribute('value')}")
                except:
                    pass
            elif field["type"] == "select":
                try:
                    select = contact_page._get_field(field["name"])
                    select = Select(select)
                    select.select_by_index(field["value"])
                    selected = select.first_selected_option
                    print(f"{field['name']}: {selected.text}")
                except:
                    pass
    
    def _clear_form(self, fields_data: list, contact_page: PageContact):
        for field in fields_data:
            if field["type"] == "input":
                try:
                    input = contact_page._get_field(field["name"])
                    input.clear()
                except:
                    pass
            elif field["type"] == "select":
                try:
                    select = contact_page._get_field(field["name"])
                    select = Select(select)
                    select.select_by_index(0)
                except:
                    pass
    
    def _test_input(self, driver, contact_page: PageContact, input_name: str, input_value, positive=True):
        form = self._get_form(driver)
        field = contact_page._get_field(input_name)
        field.clear()
        field.send_keys(input_value)
        # print('Sending form with: ', input_value)
        driver.execute_script("arguments[0].click();", contact_page.send_button)
        time.sleep(1)
        # print("Clicked!")
        try:
            # Wait for alert
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print(f"Alert text: '{alert.text}'")
            alert.accept()
        except Exception as e:
            pytest.fail(f"Expected Alert! GOt error: {e}")

        form = driver.find_element(By.ID, "arajanlat")
        input = self._get_field(input_name, form)
        class_attribute = input.get_attribute("class")
        if positive:
            if class_attribute:
                assert "invalid-field" not in class_attribute, f"Class .invalid-field not found in class: {class_attribute}"
        else:
            assert class_attribute is not None, "Element hasn't class"
            assert "invalid-field" in class_attribute, f"Class .invalid-field not found in class: {class_attribute}"
    
    def _check_fields(self, fields_data: list, contact_page: PageContact, positive=True):
        for f in fields_data:
            with allure.step(f"Check field {f['name']} {'NOT' if positive else ''} has class .invalid-field"):
                field = contact_page._get_field(field_name=f['name'])
                class_attribute = field.get_attribute("class")
                if positive:
                    if class_attribute:
                        assert "invalid-field" not in class_attribute, f"Class .invalid-field not found in class: {class_attribute}"
                else:
                    assert class_attribute is not None, "Element hasn't class"
                    assert "invalid-field" in class_attribute, f"Class .invalid-field not found in class: {class_attribute}"
    
    def _get_scode(self, session, make_full_url, auth_headers, phpsessid_driver):
        with allure.step("Get Captcha code by API"):
            session.cookies.set('PHPSESSID', phpsessid_driver)
            api_url_get_scode = make_full_url(urls_data=valid_urls_data, page="get_scode")
            response = session.get(api_url_get_scode, headers=auth_headers)
            assert response.status_code == 200
            json_data = response.json()
            assert json_data['success'] is True
            scode = json_data['data']
            assert scode != "", "Scode is empty!"
            return scode
    
    @allure.id("4")
    @pytest.mark.release_03
    @pytest.mark.positive
    @pytest.mark.parametrize("fields_data", [
        {"d_name": "Minimum values", "data": minimal_values},
        {"d_name": "Random valid values", "data": random_values},
        {"d_name": "Maximum values", "data": maximum_values}
    ])
    def test_contact_form_happy_path(self, fields_data, class_driver, make_full_url, auth_headers, session, contact_page: PageContact):
        allure.dynamic.title(f"Testing form - {fields_data['d_name']}")
        # get PHPSESSID from loaded page
        phpsessid_driver = class_driver.get_cookie('PHPSESSID')
        assert phpsessid_driver, "Can't get phpsessid"
        phpsessid_driver = phpsessid_driver['value']
        # get scode by API send (phpsessid and auth token)
        fields_data["data"].append({
            "name": "captcha", 
            "type": "input", 
            "value": self._get_scode(session, make_full_url, auth_headers, phpsessid_driver)})
        with allure.step("Fill form with valid date"):
            self._fill_form_valid_data(fields_data["data"], contact_page)
        with allure.step("Sending form"):
            class_driver.execute_script("arguments[0].click();", contact_page.send_button)
            time.sleep(2)
        with allure.step("Check Success element or Error Alert"):
            success_elements = class_driver.find_elements(By.ID, "send_email_success")
            if success_elements:
                contact_page.refresh_page_state()
                return
            try:
                WebDriverWait(class_driver, 1).until(EC.alert_is_present())
                alert = class_driver.switch_to.alert
                alert_text = alert.text
                alert.accept()
                contact_page.refresh_page_state()
                pytest.fail(f"Form send with errors! Alert: {alert_text}")
                
            except TimeoutException:
                contact_page.refresh_page_state()
                pytest.fail("No success element and no alert!")

    @allure.id("8")
    @pytest.mark.release_02
    @pytest.mark.negative
    @pytest.mark.parametrize("fields_data", [
        # {"d_name": "< Minimum values", "data": out_minimal_values},
        # {"d_name": "Random invalid values", "data": random_invalid},
        {"d_name": "> Maximum values", "data": out_maximum_values}
    ])
    def test_contact_form_negative(self, fields_data, class_driver, contact_page: PageContact):
        allure.dynamic.title(f"Testing form - {fields_data['d_name']}")
        fields_data["data"].append({
            "name": "captcha",
            "type": "input",
            "value": 11})
        with allure.step("Fill form with invalid date"):
            self._fill_form_valid_data(fields_data["data"], contact_page)
        with allure.step("Sending form"):
            class_driver.execute_script("arguments[0].click();", contact_page.send_button)
            time.sleep(2)
        try:
            with allure.step("Get Alert"):
                WebDriverWait(class_driver, 2).until(EC.alert_is_present())
                alert = class_driver.switch_to.alert
                # print(f"Alert: {alert.text}")
                alert.accept()
                # return True
                contact_page.refresh_page_state()
                self._check_fields(fields_data=required_inputs, contact_page=contact_page, positive=False)
        except TimeoutException:
            pytest.fail("Form send but can't find error element!")
        except Exception as e:
            pytest.fail(f"Unexpected errer: {e}")
    
    @allure.id("7")
    @allure.title("Form zero data test")
    @pytest.mark.release_03
    @pytest.mark.negative
    def test_form_empty_data(self, class_driver, contact_page: PageContact):
        with allure.step("Cleaning form"):
            self._clear_form(fields_data=required_inputs, contact_page=contact_page)
        with allure.step("Sending empty form"):
            class_driver.execute_script("arguments[0].click();", contact_page.send_button)
            time.sleep(0.5)
        try:
            with allure.step("Get Alert"):
                WebDriverWait(class_driver, 2).until(EC.alert_is_present())
                alert = class_driver.switch_to.alert
                print(f"Alert: {alert.text}")
                alert.accept()
            # return True
            contact_page.refresh_page_state()
            self._check_fields(fields_data=required_inputs, contact_page=contact_page, positive=False)
        except TimeoutException:
            pytest.fail("Form send but can't find error element!")
        except Exception as e:
            pytest.fail(f"Unexpected errer: {e}")

