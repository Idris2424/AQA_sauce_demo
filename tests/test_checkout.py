import allure
from playwright.sync_api import expect
from config.base import URL_BASE
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage


@allure.title("TC_CHECK_001: Полный успешный чекаут")
def test_check_001_full_successful_checkout(navigate_to_page):
    # 1. Добавить товар в корзину (любой)
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.add_item_to_cart()
    # 2. Перейти в корзину
    navigate_to_page.locator(".shopping_cart_link").click()
    cart_page = CartPage(navigate_to_page)
    cart_page.click_checkout()
    # 3. Заполнить форму
    checkout_page = CheckoutPage(navigate_to_page)
    checkout_page.fill_form_and_continue("Idris", "Bob", "12345")
    # 4. Проверить Overview и Finish
    checkout_page.click_finish()
    # 5. Проверить Complete
    checkout_page.check_thank_you_visible()
    # 6. Дополнительно: проверить URL
    expect(navigate_to_page).to_have_url(f"{URL_BASE + '/checkout-complete.html'}")

@allure.title("TC_CHECK_002: Чекаут с пустым First name")
def test_check_002_empty_first_name(navigate_to_page):
    InventoryPage(navigate_to_page).add_item_to_cart(0)
    navigate_to_page.locator(".shopping_cart_link").click()
    CartPage(navigate_to_page).click_checkout()
    checkout_page = CheckoutPage(navigate_to_page)
    checkout_page.fill_form_and_continue("", "Bob", "12345")
    checkout_page.check_error_contains("First Name is required")

@allure.title("TC_CHECK_003: Чекаут с пустым Last name")
def test_check_003_empty_last_name(navigate_to_page):
    InventoryPage(navigate_to_page).add_item_to_cart(0)
    navigate_to_page.locator(".shopping_cart_link").click()
    CartPage(navigate_to_page).click_checkout()
    checkout_page = CheckoutPage(navigate_to_page)
    checkout_page.fill_form_and_continue("Idris", "", "12345")
    checkout_page.check_error_contains("Last Name is required")

@allure.title("TC_CHECK_004: Чекаут с пустым Postal code")
def test_check_004_empty_postal_code(navigate_to_page):
    InventoryPage(navigate_to_page).add_item_to_cart(0)
    navigate_to_page.locator(".shopping_cart_link").click()
    CartPage(navigate_to_page).click_checkout()
    checkout_page = CheckoutPage(navigate_to_page)
    checkout_page.fill_form_and_continue("Idris", "Bob", "")
    checkout_page.check_error_contains("Postal Code is required")

@allure.title("TC_CHECK_005: Валидация Postal code (формат)")
def test_check_005_postal_code_any_format(navigate_to_page):
    InventoryPage(navigate_to_page).add_item_to_cart(0)
    navigate_to_page.locator(".shopping_cart_link").click()
    CartPage(navigate_to_page).click_checkout()
    checkout_page = CheckoutPage(navigate_to_page)
    checkout_page.fill_form_and_continue("Idris", "Bob", "ABCDE")
    # Не должно быть ошибки, переходим на Overview
    expect(navigate_to_page).to_have_url(f"{URL_BASE + '/checkout-step-two.html'}")

@allure.title("TC_CHECK_006: Возврат к корзине из шага 1 чекаута")
def test_check_006_cancel_from_step_one_returns_to_cart(navigate_to_page):
    InventoryPage(navigate_to_page).add_item_to_cart()
    navigate_to_page.locator(".shopping_cart_link").click()
    CartPage(navigate_to_page).click_checkout()
    checkout_page = CheckoutPage(navigate_to_page)
    checkout_page.click_cancel()
    # Проверяем возврат в корзину
    expect(navigate_to_page).to_have_url(f"{URL_BASE + '/cart.html'}")
    # Товар на месте
    cart_page = CartPage(navigate_to_page)
    expect(cart_page.cart_items).to_have_count(1)

@allure.title("TC_CHECK_007: Возврат к покупкам из шага 1 чекаута")
def test_check_007_cancel_from_step_one_continue_shopping(navigate_to_page):
    InventoryPage(navigate_to_page).add_item_to_cart(0)
    navigate_to_page.locator(".shopping_cart_link").click()
    cart_page = CartPage(navigate_to_page)
    cart_page.click_continue_shopping()  # возврат к покупкам
    expect(navigate_to_page).to_have_url(f"{URL_BASE + '/inventory.html'}")

@allure.title("TC_CHECK_008: Расчёт итоговой суммы")
def test_check_008_total_math(navigate_to_page):
    # Добавим два товара для проверки сумм
    inv_page = InventoryPage(navigate_to_page)
    inv_page.add_item_to_cart(0)
    inv_page.add_item_to_cart(1)  # два разных товара
    navigate_to_page.locator(".shopping_cart_link").click()
    CartPage(navigate_to_page).click_checkout()
    checkout_page = CheckoutPage(navigate_to_page)
    checkout_page.fill_form_and_continue("Idris", "Bob", "12345")
    checkout_page.verify_tax()
    item_total = checkout_page.verify_item_total(29.99)
    tax = checkout_page.verify_tax(2.40)
    total = checkout_page.get_total_numeric()
    # Total = Item total + Tax, с точностью 0.01
    assert abs(total - (item_total + tax)) < 0.01

@allure.title("TC_CHECK_009: Округление копеек (граничный случай)")
def test_check_009_rounding_edge_case(navigate_to_page):
    inv_page = InventoryPage(navigate_to_page)
    inv_page.add_item_to_cart(0)  # $29.99
    navigate_to_page.locator(".shopping_cart_link").click()
    CartPage(navigate_to_page).click_checkout()
    checkout_page = CheckoutPage(navigate_to_page)
    checkout_page.fill_form_and_continue("Idris", "Bob", "12345")
    total_text = checkout_page.get_total_text()
    # Проверим, что после запятой 2 цифры
    import re
    match = re.search(r'\$(\d+\.\d{2})', total_text)
    assert match is not None, "Total amount not formatted with 2 decimals"

@allure.title("TC_CHECK_010: Чекаут с несколькими товарами")
def test_check_010_checkout_with_multiple_items(navigate_to_page):
    inv_page = InventoryPage(navigate_to_page)
    inv_page.add_item_to_cart(0)
    inv_page.add_item_to_cart(2)  # первый и третий товары
    navigate_to_page.locator(".shopping_cart_link").click()
    CartPage(navigate_to_page).click_checkout()
    checkout_page = CheckoutPage(navigate_to_page)
    checkout_page.fill_form_and_continue("Idris", "Bob", "12345")
    # Проверяем количество товаров в Overview
    expect(checkout_page.cart_items).to_have_count(2)
    checkout_page.click_finish()
    checkout_page.check_thank_you_visible()
