import pytest
from playwright.sync_api import sync_playwright
from config.base import BROWSERS, RESOLUTIONS
from config.users import USER1_NAME, USERS_PASSWORD
from pages.login_page import LoginPage


@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
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


@pytest.fixture
def mobile_viewport(navigate_to_page):
    """Фикстура, которая переключает страницу в мобильный вид"""
    page = navigate_to_page
    page.set_viewport_size({"width": 375, "height": 812})
    yield page


@pytest.fixture
def slow_internet():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        client = page.context.new_cdp_session(page)
        client.send("Network.emulateNetworkConditions", {
        "offline": False,
        "latency": 150,
        "downloadThroughput": 750 * 1024 / 8,
        "uploadThroughput": 250 * 1024 / 8,
        "connectionType": "cellular3g"
    })
        yield page
        context.close()
        browser.close()


@pytest.fixture(params=BROWSERS, ids=BROWSERS)
def any_browser_page(request, playwright):
    browser_name = request.param
    browser_type = getattr(playwright, browser_name)
    browser = browser_type.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
    browser.close()


@pytest.fixture(params=[True, False], ids=["headless", "headed"])
def headless_page(request, playwright):
    browser = playwright.chromium.launch(headless=request.param)
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
    browser.close()

@pytest.fixture(params=RESOLUTIONS)
def resolution_page(request, playwright):
    width, height = request.param
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": width, "height": height})
    page = context.new_page()
    yield page
    context.close()
    browser.close()
