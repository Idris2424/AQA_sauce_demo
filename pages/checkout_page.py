import allure
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
        self.thank_you_message = self.page.locator(".complete-header")
        self.error_msg = self.page.locator("[data-test='error']")
        self.cancel_btn = self.page.locator("[data-test='cancel']")
        self.item_total = self.page.locator(".summary_subtotal_label")
        self.cart_items = self.page.locator(".cart_item")

    @allure.step("Нажать кнопку оформления заказа")
    def click_checkout(self):
        self.checkout.click()

    @allure.step("Заполнить поле Имя")
    def fill_first_name(self, first_name):
        self.first_name_field.fill(first_name)

    @allure.step("Заполнить поле Фамилия")
    def fill_last_name(self, last_name):
        self.last_name_field.fill(last_name)

    @allure.step("Заполнить поле Почтовый индекс")
    def fill_postal_code(self, postal_code):
        self.postal_code_field.fill(postal_code)

    @allure.step("Нажать кнопку Продолжить")
    def click_continue_btn(self):
        self.continue_button.click()

    @allure.step("Проверить значение поля Имя")
    def check_first_name(self, first_name):
        expect(self.first_name_field).to_have_value(first_name)

    @allure.step("Проверить значение поля Фамилия")
    def check_last_name(self, last_name):
        expect(self.last_name_field).to_have_value(last_name)

    @allure.step("Проверить значение поля Почтовый индекс")
    def check_postal_code(self, postal_code):
        expect(self.postal_code_field).to_have_value(postal_code)

    @allure.step("Проверить товары на странице оформления")
    def check_inventory_in_checkout(self):
        backpack = self.page.locator("text=Sauce Labs Backpack")
        assert backpack.count() == 1, "Товар Sauce Labs Backpack не найден"

        items = self.page.locator(".summary_item, .cart_item").all()
        assert len(items) == 1, f"Найдено товаров: {len(items)}"

    @allure.step("Проверить цену на странице оформления")
    def check_price_in_checkout(self):
        assert self.checkout_price.inner_text() == "Item total: $29.99"

    @allure.step("Проверить информацию об оплате")
    def verify_payment_information(self, expected_text="SauceCard #31337"):
        expect(self.payment_info_value).to_contain_text(expected_text)

    @allure.step("Проверить информацию о доставке")
    def verify_shipping_information(self, expected_text="Free Pony Express Delivery!"):
        expect(self.shipping_info_value).to_contain_text(expected_text)

    @allure.step("Проверить сумму товаров")
    def verify_item_total(self, saved_price_numeric):
        subtotal_text = self.checkout_price.inner_text()
        item_total = float(subtotal_text.split("$")[1])
        assert item_total == saved_price_numeric
        return item_total

    @allure.step("Проверить налог")
    def verify_tax(self, expected_tax=2.40):
        expect(self.tax_label).to_have_text(f"Tax: ${expected_tax:.2f}")
        return expected_tax

    @allure.step("Проверить итоговую сумму")
    def verify_total(self, item_total, tax):
        total_text = self.total_label.inner_text()
        total_value = float(total_text.split("$")[1])
        expected_total = round(item_total + tax, 2)
        assert abs(total_value - expected_total) < 0.01

    @allure.step("Нажать кнопку Завершить заказ")
    def click_finish(self):
        self.finish_button.click()
        self.page.wait_for_url("**/checkout-complete.html")

    @allure.step("Заполнить форму и нажать Продолжить")
    def fill_form_and_continue(self, first, last, zip_code):
        self.fill_first_name(first)
        self.fill_last_name(last)
        self.fill_postal_code(zip_code)
        self.click_continue_btn()

    @allure.step("Проверить сообщение благодарности")
    def check_thank_you_visible(self):
        expect(self.thank_you_message).to_be_visible()

    @allure.step("Проверить сообщение об ошибке")
    def check_error_contains(self, expected_text: str):
        expect(self.error_msg).to_contain_text(expected_text)

    @allure.step("Нажать кнопку Отмена")
    def click_cancel(self):
        self.cancel_btn.click()

    @allure.step("Получить текст итоговой суммы")
    def get_total_text(self) -> str:
        return self.total_label.text_content()

    @allure.step("Получить итоговую сумму числом")
    def get_total_numeric(self) -> float:
        text = self.get_total_text()
        return float(text.split("$")[1])

    @allure.step("Получить налог числом")
    def get_tax_numeric(self):
        tax_text = self.tax_label.inner_text()
        return float(tax_text.split("$")[1])
