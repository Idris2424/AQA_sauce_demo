from playwright.sync_api import expect
from config.base import URL_BASE


class BasePage:
    def __init__(self, page):
        self.page = page

    def open(self, url=URL_BASE):
        self.page.goto(url)

    def get_current_url(self):
        return self.page.current_url

    def expect_to_have_url(self, url_sub: str):
        expect(self.page).to_have_url(URL_BASE + url_sub)

    def check_404_page(self, url="https://www.saucedemo.com/fdgfgdsgsdgf"):
        response = self.page.goto(url)
        assert response.status == 404
        expect(self.page.locator("body")).to_contain_text("404")
        return response