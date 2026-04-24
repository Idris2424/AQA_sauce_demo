import pytest
from playwright.sync_api import expect
from config.base import URL_BASE, URL_BASE_ROOT, ERROR_MSG_LOGIN_USERNAME, ERROR_MSG_LOGIN_PASSWORD
from config.users import USER1_NAME, USERS_PASSWORD
from pages.login_page import LoginPage


# ---- TC_AUTH_001 ----
def test_valid_login_standard_user(page):
    login_page = LoginPage(page)
    # Шаг 1 Перейти на главную страницу (аутентификация)
    login_page.open()
    expect(page).to_have_url(URL_BASE_ROOT)
    # Шаг 2	Ввести имя
    login_page.fill_username(USER1_NAME)
    login_page.check_username(USER1_NAME)
    # Шаг 3	Ввести пароль
    login_page.fill_password(USERS_PASSWORD)
    login_page.check_password(USERS_PASSWORD)
    # Шаг 4	Нажать Login
    login_page.click_login_button()
    expect(page).to_have_url(f"{URL_BASE + '/inventory.html'}")

# ---- TC_AUTH_002 ----
@pytest.mark.parametrize("username", ["problem_user", "performance_glitch_user"])
def test_valid_login_other_users(page, username):
    login_page = LoginPage(page)
    login_page.open()
    login_page.fill_username(username)
    login_page.fill_password(USERS_PASSWORD)
    login_page.click_login_button()
    expect(page).to_have_url(f"{URL_BASE + "/inventory.html"}")

# ---- TC_AUTH_003 ----
def test_invalid_password(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.fill_username(USER1_NAME)
    login_page.fill_password("Wrong password")
    login_page.click_login_button()
    assert login_page.check_error_with_msg()

# ---- TC_AUTH_004 ----
def test_nonexistent_username(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.fill_username("fake_user")
    login_page.fill_password(USERS_PASSWORD)
    login_page.click_login_button()
    assert login_page.check_error_with_msg()

# ---- TC_AUTH_005 ----
def test_empty_username(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.fill_username("")
    login_page.fill_password(USERS_PASSWORD)
    login_page.click_login_button()
    assert login_page.check_error_with_msg(ERROR_MSG_LOGIN_USERNAME)


# ---- TC_AUTH_006 ----
def test_empty_password(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.fill_username(USER1_NAME)
    login_page.fill_password("")
    login_page.click_login_button()
    assert login_page.check_error_with_msg(ERROR_MSG_LOGIN_PASSWORD)

# ---- TC_AUTH_007 ----
def test_sql_injection(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.fill_username("' OR '1'='1")
    login_page.fill_password("anything")
    login_page.click_login_button()
    assert login_page.check_error_with_msg()


# ---- TC_AUTH_008 ----
def test_xss_attempt(page):
    login_page = LoginPage(page)
    login_page.open()
    xss_payload = "<script>alert(1)</script>"
    login_page.fill_username(xss_payload)
    login_page.fill_password("anything")
    login_page.check_username(xss_payload)
    login_page.click_login_button()
    assert login_page.check_error_with_msg()

# ---- TC_AUTH_009 ----
def test_no_account_lockout_after_failed_attempts(page):
    login_page = LoginPage(page)
    login_page.open()

    for _ in range(5):
        login_page.fill_username(USER1_NAME)
        login_page.fill_password("Wrong password")
        login_page.clear_login_fields()

    # 6-я попытка с правильным паролем
    login_page.fill_username(USER1_NAME)
    login_page.fill_password(USERS_PASSWORD)
    login_page.click_login_button()
    expect(page).to_have_url(f"{URL_BASE + '/inventory.html'}")


# ---- TC_AUTH_010 ----
def test_session_persists_after_reload(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.fill_username(USER1_NAME)
    login_page.fill_password(USERS_PASSWORD)
    login_page.click_login_button()
    expect(page).to_have_url(f"{URL_BASE + '/inventory.html'}")
    # Перезагрузка страницы
    page.reload()
    # Проверяем, что сессия активна: URL остался и виден логотип Swag Labs
    expect(page).to_have_url(f"{URL_BASE + '/inventory.html'}")
    login_page.check_logo()
