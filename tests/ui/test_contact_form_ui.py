import pytest
import allure
from test_data.send_message_data import required_inputs
from pages.page_contact import PageContact


@allure.epic("User")
@allure.story('User can send message')
class TestContactFormUI:

    @allure.id("1")
    @pytest.mark.ui
    @pytest.mark.release_03
    @pytest.mark.parametrize("field", required_inputs)
    def test_ui_form_test(self, field, contact_page: PageContact):
        # form = self._get_form(class_driver)
        allure.dynamic.title(f"UI form test: {field['type']} {field['name']}")
        founded_field = contact_page._get_field(field_name=field['name'])
        if "props" in field:
            contact_page._check_field_proprs(field=founded_field, props=field["props"])