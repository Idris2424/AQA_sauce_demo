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
        self.payment_info_value = self.page.locator('[data-test="payment-info-value"]')
        self.shipping_info_value = self.page.locator('[data-test="shipping-info-value"]')
        self.tax_label = self.page.locator(".summary_tax_label")
        self.total_label = self.page.locator(".summary_total_label")
        self.finish_button = self.page.locator("#finish")

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

    def verify_payment_information(self, expected_text="SauceCard #31337"):
        expect(self.payment_info_value).to_contain_text(expected_text)

    def verify_shipping_information(self, expected_text="Free Pony Express Delivery!"):
        expect(self.shipping_info_value).to_contain_text(expected_text)

    def verify_item_total(self, saved_price_numeric):
        subtotal_text = self.checkout_price.inner_text()
        item_total = float(subtotal_text.split("$")[1])
        assert item_total == saved_price_numeric
        return item_total

    def verify_tax(self, expected_tax=2.40):
        expect(self.tax_label).to_have_text(f"Tax: ${expected_tax:.2f}")
        return expected_tax

    def verify_total(self, item_total, tax):
        total_text = self.total_label.inner_text()
        total_value = float(total_text.split("$")[1])
        expected_total = round(item_total + tax, 2)
        assert abs(total_value - expected_total) < 0.01

    def click_finish(self):
        self.finish_button.click()
        self.page.wait_for_url("**/checkout-complete.html")
