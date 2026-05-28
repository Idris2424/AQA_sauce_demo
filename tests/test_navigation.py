import allure
import pytest
from playwright.sync_api import expect
from config.base import INVENTORY_URL
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytestmark = [allure.label("feature", "Навигация")]



@allure.title("TC_UI_001: Логотип кликабелен → возврат на главную")
def test_ui_001_logo_returns_to_main(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.click_logo()
    expect(navigate_to_page).to_have_url(INVENTORY_URL)

@allure.title("TC_UI_002: Меню гамбургер – открыть/закрыть, пункты работают")
def test_ui_002_burger_menu(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.open_burger_menu()
    assert inventory_page.is_burger_menu_visible()
    inventory_page.click_menu_item()
    expect(navigate_to_page).to_have_url(INVENTORY_URL)
    inventory_page.close_burger_menu()

@allure.title("TC_UI_003: Адаптивность – мобильная вёрстка")
def test_ui_003_mobile_responsive(mobile_viewport):
    inventory_page = InventoryPage(mobile_viewport)
    inventory_page.open_basket()
    inventory_page.verify_cart_btn()

@allure.title("TC_UI_004: Тёмная тема (не поддерживается SauceDemo)")
def test_ui_004_dark_theme(navigate_to_page):
    pytest.skip("SauceDemo не поддерживает тёмную тему.")

@allure.title("TC_UI_005: Локализация интерфейса (не поддерживается)")
def test_ui_005_localization(navigate_to_page):
    pytest.skip("На SauceDemo нет переключения языка")

@allure.title("TC_UI_006: Состояния кнопок disabled/enabled на форме логина")
def test_ui_006_button_states(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.fill_username("user")
    login_page.fill_password("pass")
    assert login_page.is_login_button_enabled()

@allure.title("TC_UI_007: Фокус на полях ввода (Tab-навигация)")
def test_ui_007_focus_visible(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.press_tab()
    login_page.get_focused_element_id()
    login_page.verify_focus()

@allure.title("TC_UI_008: ARIA-атрибуты для скринридеров")
def test_ui_008_aria_attributes(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.check_burger_btn_has_aria_attributes()
    inventory_page.check_cart_has_aria_attributes()

@allure.title("TC_UI_009: Индикатор загрузки (лоадер) – на SauceDemo нет")
def test_ui_009_loader_visible(navigate_to_page):
    pytest.skip("SauceDemo не использует лоадеры.")

@allure.title("TC_UI_010: Обработка 404 на несуществующем URL")
def test_ui_010_not_found_page(navigate_to_page):
    check_404_page(navigate_to_page)