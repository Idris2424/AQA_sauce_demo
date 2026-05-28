import allure
from playwright.sync_api import expect
from config.base import *
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage

pytestmark = [allure.label("feature", "Чекаут")]



@allure.title("TC_CHECK_001: Полный успешный чекаут")
def test_check_001_full_successful_checkout(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.add_item_to_cart()
    inventory_page.go_to_cart()
    cart_page = CartPage(navigate_to_page)
    cart_page.click_checkout()
    checkout_page = CheckoutPage(navigate_to_page)
    checkout_page.fill_form_and_continue("Idris", "Bob", "12345")
    checkout_page.click_finish()
    checkout_page.check_thank_you_visible()
    expect(navigate_to_page).to_have_url(CHECKOUT_COMPLETE_URL)

@allure.title("TC_CHECK_002: Чекаут с пустым First name")
def test_check_002_empty_first_name(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.add_item_to_cart()
    inventory_page.go_to_cart()
    CartPage(navigate_to_page).click_checkout()
    checkout_page = CheckoutPage(navigate_to_page)
    checkout_page.fill_form_and_continue("", "Bob", "12345")
    checkout_page.check_error_contains("First Name is required")

@allure.title("TC_CHECK_003: Чекаут с пустым Last name")
def test_check_003_empty_last_name(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.add_item_to_cart()
    inventory_page.go_to_cart()
    CartPage(navigate_to_page).click_checkout()
    checkout_page = CheckoutPage(navigate_to_page)
    checkout_page.fill_form_and_continue("Idris", "", "12345")
    checkout_page.check_error_contains("Last Name is required")

@allure.title("TC_CHECK_004: Чекаут с пустым Postal code")
def test_check_004_empty_postal_code(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.add_item_to_cart()
    inventory_page.go_to_cart()
    CartPage(navigate_to_page).click_checkout()
    checkout_page = CheckoutPage(navigate_to_page)
    checkout_page.fill_form_and_continue("Idris", "Bob", "")
    checkout_page.check_error_contains("Postal Code is required")

@allure.title("TC_CHECK_005: Валидация Postal code (формат)")
def test_check_005_postal_code_any_format(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.add_item_to_cart()
    inventory_page.go_to_cart()
    CartPage(navigate_to_page).click_checkout()
    checkout_page = CheckoutPage(navigate_to_page)
    checkout_page.fill_form_and_continue("Idris", "Bob", "ABCDE")
    expect(navigate_to_page).to_have_url(CHECKOUT_STEP_ONE_URL)

@allure.title("TC_CHECK_006: Возврат к корзине из шага 1 чекаута")
def test_check_006_cancel_from_step_one_returns_to_cart(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.add_item_to_cart()
    inventory_page.go_to_cart()
    CartPage(navigate_to_page).click_checkout()
    checkout_page = CheckoutPage(navigate_to_page)
    checkout_page.click_cancel()
    expect(navigate_to_page).to_have_url(CART_URL)
    cart_page = CartPage(navigate_to_page)
    expect(cart_page.cart_items).to_have_count(1)

@allure.title("TC_CHECK_007: Возврат к покупкам из шага 1 чекаута")
def test_check_007_cancel_from_step_one_continue_shopping(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.add_item_to_cart()
    inventory_page.go_to_cart()
    cart_page = CartPage(navigate_to_page)
    cart_page.click_continue_shopping()
    expect(navigate_to_page).to_have_url(INVENTORY_URL)

@allure.title("TC_CHECK_008: Расчёт итоговой суммы")
def test_check_008_total_math(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.add_item_to_cart(0)
    inventory_page.add_item_to_cart(1)
    inventory_page.go_to_cart()
    CartPage(navigate_to_page).click_checkout()
    checkout_page = CheckoutPage(navigate_to_page)
    checkout_page.fill_form_and_continue("Idris", "Bob", "12345")
    subtotal_text = checkout_page.checkout_price.inner_text()
    item_total = float(subtotal_text.split("$")[1])
    tax = checkout_page.get_tax_numeric()
    total = checkout_page.get_total_numeric()
    assert abs(total - (item_total + tax)) < 0.01

@allure.title("TC_CHECK_009: Округление копеек (граничный случай)")
def test_check_009_rounding_edge_case(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.add_item_to_cart(0)
    inventory_page.go_to_cart()
    CartPage(navigate_to_page).click_checkout()
    checkout_page = CheckoutPage(navigate_to_page)
    checkout_page.fill_form_and_continue("Idris", "Bob", "12345")
    total_text = checkout_page.get_total_text()
    import re
    match = re.search(r'\$(\d+\.\d{2})', total_text)
    assert match is not None, "Total amount not formatted with 2 decimals"

@allure.title("TC_CHECK_010: Чекаут с несколькими товарами")
def test_check_010_checkout_with_multiple_items(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.add_item_to_cart(0)
    inventory_page.add_item_to_cart(2)
    inventory_page.go_to_cart()
    CartPage(navigate_to_page).click_checkout()
    checkout_page = CheckoutPage(navigate_to_page)
    checkout_page.fill_form_and_continue("Idris", "Bob", "12345")
    expect(checkout_page.cart_items).to_have_count(2)
    checkout_page.click_finish()
    checkout_page.check_thank_you_visible()
