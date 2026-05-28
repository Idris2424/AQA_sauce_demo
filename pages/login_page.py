import allure
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
        self.burger_menu = self.page.locator("#react-burger-menu-btn")
        self.logout_link = self.page.locator("#logout_sidebar_link")

    @allure.step("Заполнить поле Имя пользователя")
    def fill_username(self, username):
        self.field_username.fill(username)

    @allure.step("Заполнить поле Пароль")
    def fill_password(self, password):
        self.field_password.fill(password)

    @allure.step("Нажать кнопку Войти")
    def click_login_button(self):
        self.login_button.click()

    @allure.step("Проверить значение поля Имя пользователя")
    def check_username(self, username):
        expect(self.field_username).to_have_value(username)

    @allure.step("Проверить значение поля Пароль")
    def check_password(self, password):
        expect(self.field_password).to_have_value(password)

    @allure.step("Выполнить вход в систему")
    def login_procedure(self, username, password):
        self.fill_username(username)
        self.fill_password(password)
        self.click_login_button()

    @allure.step("Проверить сообщение об ошибке входа")
    def check_error_with_msg(self, error_msg=ERROR_MSG_LOGIN):
        expect(self.error).to_be_visible()
        expect(self.error).to_have_text(error_msg)
        expect(self.error).to_have_css('color', 'rgb(19, 35, 34)')
        return True

    @allure.step("Очистить поля входа")
    def clear_login_fields(self):
        self.field_username.clear()
        self.field_password.clear()

    @allure.step("Проверить логотип")
    def check_logo(self):
        assert self.logo.is_visible()
        assert self.logo.text_content() == "Swag Labs"

    @allure.step("Выйти из системы")
    def logout(self):
        self.burger_menu.click()
        self.logout_link.click()

    @allure.step("Проверить активность кнопки Войти")
    def is_login_button_enabled(self):
        return self.login_button.is_enabled()

    @allure.step("Нажать клавишу Tab")
    def press_tab(self):
        self.page.keyboard.press("Tab")

    @allure.step("Получить id активного элемента")
    def get_focused_element_id(self):
        return self.page.evaluate("document.activeElement.id")

    @allure.step("Проверить фокус на поле Имя пользователя")
    def verify_focus(self):
        assert self.get_focused_element_id() == "user-name"
