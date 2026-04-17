from playwright.sync_api import expect
from pages.base_page import BasePage


class CheckoutPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.checkout = self.page.locator("#checkout")
        self.first_name_field = self.page.locator("#first-name")
        self.last_name_field = self.page.locator("#last-name")
        self.postal_code_field = self.page.locator("#postal-code")
        self.continue_button = self.page.locator("#continue")
        self.checkout_price = self.page.locator(".summary_subtotal_label")

    def click_checkout(self):
        self.checkout.click()

    def fill_first_name(self, first_name):
        self.first_name_field.fill(first_name)

    def fill_last_name(self, last_name):
        self.last_name_field.fill(last_name)

    def fill_postal_code(self, postal_code):
        self.postal_code_field.fill(postal_code)

    def click_continue_btn(self):
        self.continue_button.click()

    def check_first_name(self, first_name):
        expect(self.first_name_field).to_have_value(first_name)

    def check_last_name(self, last_name):
        expect(self.last_name_field).to_have_value(last_name)

    def check_postal_code(self, postal_code):
        expect(self.postal_code_field).to_have_value(postal_code)

    def check_inventory_in_checkout(self):
        backpack = self.page.locator("text=Sauce Labs Backpack")
        assert backpack.count() == 1, "Товар Sauce Labs Backpack не найден"

        items = self.page.locator(".summary_item, .cart_item").all()
        assert len(items) == 1, f"Найдено товаров: {len(items)}"

    def check_price_in_checkout(self):
        assert self.checkout_price.inner_text() == "Item total: $29.99"
