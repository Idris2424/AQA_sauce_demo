import allure
from pages.base_page import BasePage


class CartPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.cart_items = self.page.locator(".cart_item")
        self.qty_locator = self.page.locator(".cart_quantity")
        self.name_inventor = self.page.locator(".inventory_item_name")
        self.cart_price = self.page.locator(".inventory_item_price")
        self.continue_shopping_btn = self.page.locator("#continue-shopping")
        self.empty_cart_message = self.page.locator(".title")
        self.checkout_button = self.page.locator("[data-test='checkout']")

    @allure.step("Получить все элементы корзины")
    def all_cart_items(self):
        return self.cart_items.all()

    @allure.step("Проверить цену в корзине")
    def check_price_in_basket(self):
        assert self.cart_price == "$29.99"

    @allure.step("Удалить товар из корзины по названию")
    def remove_item_by_name(self, item_name):
        item_id = item_name.lower().replace(' ', '-')
        self.page.click(f"button[id*='remove-{item_id}']")

    @allure.step("Получить количество товаров в корзине")
    def get_cart_items_count(self):
        return self.cart_items.count()

    @allure.step("Нажать кнопку 'Продолжить покупки'")
    def click_continue_shopping(self):
        self.continue_shopping_btn.click()

    @allure.step("Проверить сообщение о пустой корзине")
    def verify_empty_message(self):
        return self.empty_cart_message.is_visible()

    @allure.step("Нажать кнопку 'Оформить заказ'")
    def click_checkout(self):
        self.checkout_button.click()

