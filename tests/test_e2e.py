from playwright.sync_api import expect

from config.base import URL_BASE
from config.users import USER1_NAME, USERS_PASSWORD, FIRST_NAME, LAST_NAME, POSTAL_CODE
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class TestCheckOut:

    def test_check001(self, page):
        # Шаг 1 Открыть сайт
        login_page = LoginPage(page)
        # Шаг 2-3	Ввести логин Ввести пароль
        login_page.fill_username_and_password(USER1_NAME, USERS_PASSWORD)
        login_page.check_field_username_and_password(USER1_NAME, USERS_PASSWORD)
        # Шаг 4 Нажать Login
        login_page.click_login_button()
        expect(page).to_have_url(f"{URL_BASE + "inventory.html"}")
        # Шаг 5 Найти товар "Sauce Labs Backpack"
        inventory_page = InventoryPage(page)
        inventory_page.check_backpack1_visible()
        # Шаг 6 Сохранить цену товара
        price1 = inventory_page.get_backpack1_price()
        inventory_page.check_is_price()
        print(f"'{price1}'")
        # Шаг 7 Нажать "Add to cart" для товара
        inventory_page.click_btn_add_to_cart()
        # Шаг 8 Проверить бейдж корзины
        inventory_page.check_cart_badge()
        # Шаг 9 Открыть корзину
        inventory_page.open_basket()
        expect(page).to_have_url(f"{URL_BASE + "cart.html"}")
        # Шаг 10 Проверить количество товаров в корзине
        cart_page = CartPage(page)
        cart_page.all_cart_items()
        assert cart_page.cart_items.count() == 1
        # Шаг 11 Проверить количество единиц товара
        expect(cart_page.qty_locator).to_have_text("1")
        # Шаг 12 Проверить название товара
        expect(cart_page.name_inventor).to_contain_text("Sauce Labs Backpack")
        # Шаг 13 Проверить цену в корзине
        cart_page.check_price_in_basket()
        # Шаг 14 Нажать Checkout
        checkout_page = CheckoutPage(page)
        checkout_page.click_checkout()
        expect(page).to_have_url(f"{URL_BASE + "checkout-step-one.html"}")
        # Шаг 15-16-17 Заполнить First name Last name Postal code
        checkout_page.fill_first_name_last_name_postal_code(FIRST_NAME, LAST_NAME, POSTAL_CODE)
        checkout_page.check_field_first_name_last_name_and_postal_code(
            FIRST_NAME, LAST_NAME, POSTAL_CODE)
        # Шаг 18 Нажать Continue
        checkout_page.click_continue_btn()
        expect(page).to_have_url(f"{URL_BASE + "checkout-step-two.html"}")
        # Шаг 19: Проверить товар на чекауте
        checkout_page.check_inventory_in_checkout()
        # Шаг 20: Проверить цену на чекауте
        checkout_page.check_price_in_checkout()


