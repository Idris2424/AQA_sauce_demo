import allure
from playwright.sync_api import expect

from config.base import INVENTORY_URL
from config.users import USER1_NAME, USERS_PASSWORD
from pages.login_page import LoginPage

pytestmark = [allure.label("feature", "Кроссбраузер")]


@allure.title("TC_XB_001_002_003: Chromium, Firefox, WebKit")
def test_tc_xb_001_002_003_browsers(any_browser_page):
    login_page = LoginPage(any_browser_page)
    login_page.open()
    login_page.login_procedure(USER1_NAME, USERS_PASSWORD)
    expect(any_browser_page).to_have_url(INVENTORY_URL)

@allure.title("TC_XB_004: Headless vs Headed")
def test_tc_xb_004_headless_vs_headed(headless_page):
    login_page = LoginPage(headless_page)
    login_page.open()
    login_page.login_procedure(USER1_NAME, USERS_PASSWORD)
    expect(headless_page).to_have_url(INVENTORY_URL)

@allure.title("TC_XB_005: Разные разрешения")
def test_tc_xb_005_resolutions(resolution_page):
    login_page = LoginPage(resolution_page)
    login_page.open()
    assert login_page.login_button.is_visible()