from playwright.sync_api import expect

from config.base import URL_BASE, URL_BASE_ROOT
from config.products import BACKPACK_NAME
from config.users import USER1_NAME, USERS_PASSWORD, FIRST_NAME, LAST_NAME, POSTAL_CODE
from pages.CompletePage import CompletePage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class TestCheckOut:

    def test_check001(self, page):
        # Шаг 1 Открыть сайт
        expect(page).to_have_url(URL_BASE_ROOT)
        # Шаг 2	Ввести логин
        login_page = LoginPage(page)
        login_page.fill_username(USER1_NAME)
        login_page.check_username(USER1_NAME)
        # Шаг 3 Ввести пароль
        login_page.fill_password(USERS_PASSWORD)
        login_page.check_password(USERS_PASSWORD)
        # Шаг 4 Нажать Login
        login_page.click_login_button()
        expect(page).to_have_url(f"{URL_BASE + "/inventory.html"}")
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
        inventory_page.check_cart_badge(1)
        # Шаг 9 Открыть корзину
        inventory_page.open_basket()
        expect(page).to_have_url(f"{URL_BASE + "/cart.html"}")
        # Шаг 10 Проверить количество товаров в корзине
        cart_page = CartPage(page)
        cart_page.all_cart_items()
        assert cart_page.cart_items.count() == 1
        # Шаг 11 Проверить количество единиц товара
        expect(cart_page.qty_locator).to_have_text("1")
        # Шаг 12 Проверить название товара
        expect(cart_page.name_inventor).to_contain_text(BACKPACK_NAME)
        # Шаг 13 Проверить цену в корзине
        cart_page.check_price_in_basket()
        # Шаг 14 Нажать Checkout
        checkout_page = CheckoutPage(page)
        checkout_page.click_checkout()
        expect(page).to_have_url(f"{URL_BASE + "/checkout-step-one.html"}")
        # Шаг 15 Заполнить First name
        checkout_page.fill_first_name(FIRST_NAME)
        checkout_page.check_first_name(FIRST_NAME)
        # Шаг 16 Заполнить Last name
        checkout_page.fill_last_name(LAST_NAME)
        checkout_page.check_last_name(LAST_NAME)
        # Шаг 17 Заполнить Postal code
        checkout_page.fill_postal_code(POSTAL_CODE)
        checkout_page.check_postal_code(POSTAL_CODE)
        # Шаг 18 Нажать Continue
        checkout_page.click_continue_btn()
        expect(page).to_have_url(f"{URL_BASE + "/checkout-step-two.html"}")
        # Шаг 19: Проверить товар на чекауте
        checkout_page.check_inventory_in_checkout()
        # Шаг 20: Проверить цену на чекауте
        checkout_page.check_price_in_checkout()
        # ШАГ 21 Проверить Payment Information
        checkout_page.verify_payment_information("SauceCard #31337")
        # ШАГ 22 Проверить Shipping Information
        checkout_page.verify_shipping_information("Free Pony Express Delivery!")
        # ШАГ 23 Проверить Item total
        item_total = checkout_page.verify_item_total(29.99)
        # ШАГ 24 Проверить Tax
        tax = checkout_page.verify_tax(2.40)
        # ШАГ 25 Проверить Total
        checkout_page.verify_total(item_total, tax)
        # ШАГ 26 Нажать Finish
        checkout_page.click_finish()
        # ШАГИ 27 Проверить заголовок успеха
        complete_page = CompletePage(page)
        complete_page.verify_success_header("Checkout: Complete!")
        # ШАГИ 28 Проверить благодарность
        complete_page.verify_thank_you_message()
        # ШАГИ 29 Проверить сообщение о доставке
        complete_page.verify_dispatch_message()
        # ШАГИ 30 Проверить кнопку Back Home
        complete_page.verify_back_home_button_visible_and_enabled()
        # ШАГИ 31 Нажать Back Home
        complete_page.click_back_home()
        assert page.url.endswith("/inventory.html")
