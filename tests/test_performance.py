import time
import allure
from playwright.sync_api import expect
from config.base import INVENTORY_URL
from config.users import USER1_NAME, USERS_PASSWORD
from pages.login_page import LoginPage

pytestmark = [allure.label("feature", "Производительность")]



@allure.title("TC_PERF_001: Время загрузки главной страницы < 3 сек")
def test_tc_perf_001_load_time(page):
    login_page = LoginPage(page)
    start = time.time()
    login_page.open()
    end = time.time()
    assert end - start < 3

@allure.title("TC_PERF_002: Клик Login -> переход < 1 сек")
def test_tc_perf_002_login_response(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.fill_username(USER1_NAME)
    login_page.fill_password(USERS_PASSWORD)
    start = time.time()
    login_page.click_login_button()
    expect(page).to_have_url(INVENTORY_URL)
    end = time.time()
    assert end - start < 1

@allure.title("TC_PERF_003: 10 последовательных прогонов без флаки")
def test_tc_perf_003_stability(page):
    for i in range(10):
        login_page = LoginPage(page)
        login_page.open()
        login_page.login_procedure(USER1_NAME, USERS_PASSWORD)

@allure.title("TC_PERF_004: Эмуляция 3G -> тест проходит без таймаутов")
def test_tc_perf_004_slow_connection(slow_internet):
    login_page = LoginPage(slow_internet)
    login_page.open()
    login_page.login_procedure(USER1_NAME, USERS_PASSWORD)
    expect(slow_internet).to_have_url(INVENTORY_URL)