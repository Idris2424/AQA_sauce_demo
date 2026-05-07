from playwright.sync_api import expect


def check_404_page(page, url: str = "https://www.saucedemo.com/fdgfgdsgsdgf"):
    response = page.goto(url)
    assert response.status == 404
    expect(page.locator("body")).to_contain_text("404")
    return response