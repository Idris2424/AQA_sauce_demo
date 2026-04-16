from playwright.sync_api import expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.field_username = self.page.locator("#user-name")
        self.field_password = self.page.locator("#password")
        self.login_button = self.page.get_by_role("button", name="Login")


    def fill_username_and_password(self, username, password):
        self.field_username.fill(username)
        self.field_password.fill(password)

    def click_login_button(self):
        self.login_button.click()

    def check_field_username_and_password(self, username, password):
        expect(self.field_username).to_have_value(username)
        expect(self.field_password).to_have_value(password)
