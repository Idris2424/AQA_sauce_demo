from playwright.sync_api import expect
from config.products import EXPECTED_NAMES, EXPECTED_PRICES
from pages.inventory_page import InventoryPage


# ---- TC_INV_001 ----
def test_inv_001_six_products_displayed(navigate_to_page):
    """Отображение всех 6 товаров"""
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.check_product_count(6)

# ---- TC_INV_002 ----
def test_inv_002_product_names_match(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    names = inventory_page.get_product_names()
    assert names == EXPECTED_NAMES

# ---- TC_INV_003 ----
def test_inv_003_product_prices_match(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    prices = inventory_page.get_product_prices()
    assert prices == EXPECTED_PRICES

# ---- TC_INV_004 ----
def test_inv_004_images_not_broken(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.check_images_not_broken()

# ---- TC_INV_005 ----
def test_inv_005_sort_price_low_to_high(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.sort_by("lohi")
    prices = inventory_page.get_product_prices()
    numeric = [float(p.replace("$", "")) for p in prices]
    assert numeric == sorted(numeric)

# ---- TC_INV_006 ----
def test_inv_006_sort_price_high_to_low(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.sort_by("hilo")
    prices = inventory_page.get_product_prices()
    numeric = [float(p.replace("$", "")) for p in prices]
    assert numeric == sorted(numeric, reverse=True)

# ---- TC_INV_007 ----
def test_inv_007_sort_name_a_to_z(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.sort_by("az")
    names = inventory_page.get_product_names()
    assert names == sorted(names)

# ---- TC_INV_008 ----
def test_inv_008_item_remains_after_sort(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.add_item_to_cart()
    inventory_page.sort_by("hilo")
    inventory_page.check_button_text(0, "Add to cart")

# ---- TC_INV_009 ----
def test_inv_009_click_on_image_navigates(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.click_product_image()
    inventory_page.verify_inventory_page_is_open()

# ---- TC_INV_010 ----
def test_inv_010_remove_button_and_cart_badge(navigate_to_page):
    inventory_page = InventoryPage(navigate_to_page)
    inventory_page.add_item_to_cart()
    inventory_page.check_button_text(0, "Remove")
    inventory_page.check_cart_badge_equals("1")
    inventory_page.remove_item_from_cart()
    inventory_page.check_cart_badge_equals("0")
