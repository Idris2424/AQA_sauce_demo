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
