import re

from playwright.sync_api import expect

from config.products import BACKPACK_NAME
from pages.base_page import BasePage


class InventoryPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.backpack1 = self.page.get_by_text(BACKPACK_NAME)
        self.price = self.page.locator(f".inventory_item:has-text('{BACKPACK_NAME}') .inventory_item_price")
        self.btn_add_to_card = self.page.locator("#add-to-cart-sauce-labs-backpack")
        self.cart_badge = self.page.locator(".shopping_cart_badge")
        self.basket = self.page.locator(".shopping_cart_link")
        self.product_cards = self.page.locator(".inventory_item")
        self.product_names = self.page.locator(".inventory_item_name")
        self.product_prices = self.page.locator(".inventory_item_price")
        self.product_images = self.page.locator(".inventory_item_img img")
        self.sort_dropdown = self.page.locator(".product_sort_container")
        self.add_remove_buttons = self.page.locator(".btn_inventory")
        self.image_links = self.page.locator(".inventory_item_img a")


    def check_backpack1_visible(self):
        expect(self.backpack1).to_be_visible()

    def get_backpack1_price(self) -> str:
        price_ = self.price.inner_text()
        return price_

    def check_is_price(self):
        assert self.get_backpack1_price().startswith("$")

    def click_btn_add_to_cart(self):
        self.btn_add_to_card.click()

    def check_cart_badge(self, num):
        expect(self.cart_badge).to_contain_text(str(num))

    def open_basket(self):
        self.basket.click()

    def check_product_count(self, expected: int):
        expect(self.product_cards).to_have_count(expected)

    def get_product_names(self):
        return self.product_names.all_text_contents()

    def get_product_prices(self):
        return self.product_prices.all_text_contents()

    def check_images_not_broken(self):
        """Проверка что все изображения имеют src и размеры > 0"""
        images = self.product_images
        for i in range(images.count()):
            img = images.nth(i)
            src = img.get_attribute("src")
            assert src and src != "", f"Image {i} has no src"

    def sort_by(self, value):
        self.sort_dropdown.select_option(value)

    def add_item_to_cart(self, index: int = 0):
        self.add_remove_buttons.nth(index).click()

    def check_button_text(self, index, expected_text):
        expect(self.add_remove_buttons.nth(index)).to_have_text(expected_text)

    def click_product_image(self, index: int = 0):
        self.image_links.nth(index).click()

    def verify_inventory_page_is_open(self):
        expect(self.page).to_have_url(re.compile(r".*/inventory-item.html"))

    def check_cart_badge_equals(self, expected: str):
        if expected == "0" or expected == 0:
            expect(self.cart_badge).to_be_hidden()
        else:
            expect(self.cart_badge).to_have_text(str(expected))

    def remove_item_from_cart(self, index: int = 0):
        self.add_remove_buttons.nth(index).click()
