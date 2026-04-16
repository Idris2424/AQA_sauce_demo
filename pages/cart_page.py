from pages.base_page import BasePage


class CartPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.cart_items = self.page.locator(".cart_item")
        self.qty_locator = self.page.locator(".cart_quantity")
        self.name_inventor = self.page.locator(".inventory_item_name")
        self.cart_price = self.page.locator(".inventory_item_price").inner_text()

    def all_cart_items(self):
        return self.cart_items.all()

    def check_price_in_basket(self):
        assert self.cart_price == "$29.99"
