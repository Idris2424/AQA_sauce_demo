import re

import allure
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
        self.cart_icon = self.page.locator(".shopping_cart_link")
        self.logo = self.page.locator(".app_logo")
        self.burger_btn = self.page.locator("#react-burger-menu-btn")
        self.manu_all_items = self.page.locator("#inventory_sidebar_link")
        self.manu_about = self.page.locator("#about_sidebar_link")
        self.manu_logout = self.page.locator("#logout_sidebar_link")
        self.burger_close = self.page.locator("#react-burger-cross-btn")

    @allure.step("Проверить видимость рюкзака")
    def check_backpack1_visible(self):
        expect(self.backpack1).to_be_visible()

    @allure.step("Получить цену рюкзака")
    def get_backpack1_price(self) -> str:
        price_ = self.price.inner_text()
        return price_

    @allure.step("Проверить формат цены")
    def check_is_price(self):
        assert self.get_backpack1_price().startswith("$")

    @allure.step("Нажать кнопку Добавить в корзину")
    def click_btn_add_to_cart(self):
        self.btn_add_to_card.click()

    @allure.step("Проверить счётчик корзины")
    def check_cart_badge(self, num):
        expect(self.cart_badge).to_contain_text(str(num))

    @allure.step("Открыть корзину")
    def open_basket(self):
        self.basket.click()

    @allure.step("Проверить количество товаров")
    def check_product_count(self, expected: int):
        expect(self.product_cards).to_have_count(expected)

    @allure.step("Получить названия товаров")
    def get_product_names(self):
        return self.product_names.all_text_contents()

    @allure.step("Получить цены товаров")
    def get_product_prices(self):
        return self.product_prices.all_text_contents()

    @allure.step("Проверить что изображения не сломаны")
    def check_images_not_broken(self):
        """Проверка что все изображения имеют src и размеры > 0"""
        images = self.product_images
        for i in range(images.count()):
            img = images.nth(i)
            src = img.get_attribute("src")
            assert src and src != "", f"Image {i} has no src"

    @allure.step("Сортировать товары")
    def sort_by(self, value):
        self.sort_dropdown.select_option(value)

    @allure.step("Добавить товар в корзину")
    def add_item_to_cart(self, index: int = 0):
        self.add_remove_buttons.nth(index).click()

    @allure.step("Проверить текст кнопки")
    def check_button_text(self, index, expected_text):
        expect(self.add_remove_buttons.nth(index)).to_have_text(expected_text)

    @allure.step("Нажать на изображение товара")
    def click_product_image(self, index: int = 0):
        self.image_links.nth(index).click()

    @allure.step("Проверить что открыта страница товара")
    def verify_inventory_page_is_open(self):
        expect(self.page).to_have_url(re.compile(r".*/inventory-item.html"))

    @allure.step("Проверить счётчик корзины равен значению")
    def check_cart_badge_equals(self, expected: str):
        if expected == "0" or expected == 0:
            expect(self.cart_badge).to_be_hidden()
        else:
            expect(self.cart_badge).to_have_text(str(expected))

    @allure.step("Удалить товар из корзины")
    def remove_item_from_cart(self, index: int = 0):
        self.add_remove_buttons.nth(index).click()

    @allure.step("Добавить товар в корзину по названию")
    def add_item_to_cart_by_name(self, item_name):
        item_id = item_name.lower().replace(' ', '-')
        self.page.click(f"#add-to-cart-{item_id}")

    @allure.step("Добавить товар несколько раз")
    def add_item_multiple_times(self, item_name, times):
        for _ in range(times):
            self.btn_add_to_card.click()
            self.add_remove_buttons.nth(0).click()
        self.btn_add_to_card.click()

    @allure.step("Перейти в корзину")
    def go_to_cart(self):
        self.cart_icon.click()

    @allure.step("Нажать на логотип")
    def click_logo(self):
        self.logo.click()

    @allure.step("Открыть бургер-меню")
    def open_burger_menu(self):
        self.burger_btn.click()

    @allure.step("Нажать пункт меню Все товары")
    def click_menu_item(self):
        self.manu_all_items.click()

    @allure.step("Закрыть бургер-меню")
    def close_burger_menu(self):
        self.burger_close.click()

    @allure.step("Проверить видимость пунктов бургер-меню")
    def is_burger_menu_visible(self):
        return (self.manu_all_items.is_visible(),
        self.manu_about.is_visible(),
        self.manu_logout.is_visible())

    @allure.step("Проверить кнопку корзины")
    def verify_cart_btn(self):
        expect(self.basket).to_be_visible()
        expect(self.basket).to_be_enabled()

    @allure.step("Проверить aria-атрибуты кнопки меню")
    def check_burger_btn_has_aria_attributes(self):
        expect(self.burger_btn).to_have_attribute("aria-label", "Open Menu")

    @allure.step("Проверить aria-атрибуты корзины")
    def check_cart_has_aria_attributes(self):
        expect(self.basket).to_have_attribute("aria-label", "Cart")