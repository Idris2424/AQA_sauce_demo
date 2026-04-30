import allure

from pages.base_page import BasePage


class CartPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.cart_items = self.page.locator(".cart_item")
        self.qty_locator = self.page.locator(".cart_quantity")
        self.name_inventor = self.page.locator(".inventory_item_name")
        self.cart_price = self.page.locator(".inventory_item_price").inner_text()
        self.continue_shopping_btn = self.page.locator("#continue-shopping")
        self.empty_cart_message = self.page.locator(".title")

    @allure.step("Get all cart items")
    def all_cart_items(self):
        return self.cart_items.all()

    @allure.step("Check price in basket")
    def check_price_in_basket(self):
        assert self.cart_price == "$29.99"

    @allure.step("Remove item from basket")
    def remove_item_by_name(self, item_name):
        item_id = item_name.lower().replace(' ', '-')
        self.page.click(f"button[id*='remove-{item_id}']")

    @allure.step("Get cart items count")
    def get_cart_items_count(self):
        return self.cart_items.count()

    @allure.step("Click continue-shopping button")
    def click_continue_shopping(self):
        self.continue_shopping_btn.click()

    @allure.step("Verify cart empty message")
    def verify_empty_message(self):
        return self.empty_cart_message.is_visible()

