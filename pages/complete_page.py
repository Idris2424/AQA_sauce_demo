from playwright.sync_api import expect
from pages.base_page import BasePage


class CompletePage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.complete_header = self.page.locator('[data-test="title"]')
        self.thank_you_text = self.page.locator("text=Thank you for your order!")
        self.dispatch_text = self.page.locator("text=Your order has been dispatched")
        self.back_home_button = self.page.locator("#back-to-products")

    def verify_success_header(self, expected_text="Checkout: Complete!"):
        expect(self.complete_header).to_have_text(expected_text)

    def verify_thank_you_message(self):
        expect(self.thank_you_text).to_be_visible()

    def verify_dispatch_message(self):
        expect(self.dispatch_text).to_contain_text("dispatched")

    def verify_back_home_button_visible_and_enabled(self):
        expect(self.back_home_button).to_be_visible()
        expect(self.back_home_button).to_be_enabled()

    def click_back_home(self):
        self.back_home_button.click()
        self.page.wait_for_url("**/inventory.html")
