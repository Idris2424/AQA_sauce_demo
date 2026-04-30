import allure
from playwright.sync_api import expect

from config.base import URL_BASE
from config.products import BACKPACK_NAME, BIKE_LIGHT_NAME, BOLT_T_SHIRT_NAME
from config.users import USER1_NAME, USERS_PASSWORD, USER2_NAME
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@allure.title("TC_CART_001: Добавление одного товара")
def test_cart_001(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login_procedure(USER1_NAME, USERS_PASSWORD)

    inventory_page = InventoryPage(page)
    inventory_page.click_btn_add_to_cart()
    inventory_page.check_cart_badge("1")

@allure.title("TC_CART_002: Добавление нескольких разных товаров")
def test_cart_002(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login_procedure(USER1_NAME, USERS_PASSWORD)

    inventory_page = InventoryPage(page)
    inventory_page.add_item_to_cart_by_name(BACKPACK_NAME)
    inventory_page.add_item_to_cart_by_name(BIKE_LIGHT_NAME)
    inventory_page.add_item_to_cart_by_name(BOLT_T_SHIRT_NAME)
    inventory_page.check_cart_badge("3")


@allure.title("TC_CART_003: Добавление одного товара несколько раз")
def test_cart_003(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login_procedure(USER1_NAME, USERS_PASSWORD)

    inventory_page = InventoryPage(page)
    inventory_page.add_item_multiple_times(BACKPACK_NAME, 3)
    inventory_page.check_cart_badge("1")

@allure.title("TC_CART_004: Удаление товара из корзины")
def test_cart_004(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login_procedure(USER1_NAME, USERS_PASSWORD)

    inventory_page = InventoryPage(page)
    inventory_page.add_item_to_cart_by_name(BACKPACK_NAME)
    inventory_page.open_basket()

    cart_page = CartPage(page)
    cart_page.remove_item_by_name(BACKPACK_NAME)
    assert cart_page.get_cart_items_count() == 0


@allure.title("TC_CART_005: Изменение количества товара (если есть +/-)")
def test_cart_005(page):
    pass # Нету Увеличитель/уменьшитель qty


@allure.title("TC_CART_006: Переход в корзину с любой страницы")
def test_cart_006(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login_procedure(USER1_NAME, USERS_PASSWORD)

    inventory_page = InventoryPage(page)
    inventory_page.open_basket()
    expect(page).to_have_url(f"{URL_BASE + '/cart.html'}")


@allure.title("TC_CART_007: Возврат к покупкам из корзины")
def test_cart_007(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login_procedure(USER1_NAME, USERS_PASSWORD)

    inventory_page = InventoryPage(page)
    inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
    inventory_page.open_basket()

    cart_page = CartPage(page)
    cart_page.click_continue_shopping()
    expect(page).to_have_url(f"{URL_BASE + '/inventory.html'}")


@allure.title("TC_CART_008: Пустая корзина: отображение сообщения")
def test_cart_008(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login_procedure(USER1_NAME, USERS_PASSWORD)

    inventory_page = InventoryPage(page)
    inventory_page.open_basket()

    cart_page = CartPage(page)
    cart_page.verify_empty_message()


@allure.title("TC_CART_009: Сохранение корзины после перезагрузки")
def test_cart_009(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login_procedure(USER1_NAME, USERS_PASSWORD)

    inventory_page = InventoryPage(page)
    inventory_page.add_item_to_cart_by_name(BACKPACK_NAME)
    page.reload()

    inventory_page = InventoryPage(page)
    inventory_page.check_cart_badge("1")
    inventory_page.open_basket()
    cart_page = CartPage(page)
    assert cart_page.get_cart_items_count() == 1


@allure.title("TC_CART_010: Корзина при смене пользователя")
def test_cart_010(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login_procedure(USER1_NAME, USERS_PASSWORD)

    inventory_page = InventoryPage(page)
    inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")

    login_page.logout()

    login_page.login_procedure(USER2_NAME, USERS_PASSWORD)

    inventory_page = InventoryPage(page)
    assert inventory_page.cart_badge.count() == 1
