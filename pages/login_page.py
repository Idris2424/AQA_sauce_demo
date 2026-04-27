from playwright.sync_api import expect

from config.base import URL_BASE, ERROR_MSG_LOGIN
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.field_username = self.page.locator("#user-name")
        self.field_password = self.page.locator("#password")
        self.login_button = self.page.get_by_role("button", name="Login")
        self.error = self.page.locator(".error-message-container")
        self.logo = self.page.locator(".app_logo")


    def fill_username(self, username):
        self.field_username.fill(username)

    def fill_password(self, password):
        self.field_password.fill(password)

    def click_login_button(self):
        self.login_button.click()

    def check_username(self, username):
        expect(self.field_username).to_have_value(username)

    def check_password(self, password):
        expect(self.field_password).to_have_value(password)

    def login_procedure(self, username, password):
        self.fill_username(username)
        self.fill_password(password)
        self.click_login_button()

    def check_error_with_msg(self, error_msg=ERROR_MSG_LOGIN):
        expect(self.error).to_be_visible()
        expect(self.error).to_have_text(error_msg)
        expect(self.error).to_have_css('color', 'rgb(19, 35, 34)')
        return True

    def clear_login_fields(self):
        self.field_username.clear()
        self.field_password.clear()

    def check_logo(self):
        assert self.logo.is_visible()
        assert self.logo.text_content() == "Swag Labs"