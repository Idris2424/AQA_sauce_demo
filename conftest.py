import pytest
from playwright.sync_api import sync_playwright

from config.users import USER1_NAME, USERS_PASSWORD
from pages.login_page import LoginPage


@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_default_timeout(3_000)
        yield page
        browser.close()


@pytest.fixture
def navigate_to_page(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.fill_username(USER1_NAME)
    login_page.fill_password(USERS_PASSWORD)
    login_page.click_login_button()
    yield page
