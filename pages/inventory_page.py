from playwright.sync_api import expect
from pages.base_page import BasePage


class InventoryPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.backpack1 = self.page.get_by_text("Sauce Labs Backpack")
        self.price = self.page.locator(".inventory_item:has-text('Sauce Labs Backpack') .inventory_item_price")
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

    def check_cart_badge(self):
        expect(self.cart_badge).to_contain_text("1")

    def open_basket(self):
        self.basket.click()
