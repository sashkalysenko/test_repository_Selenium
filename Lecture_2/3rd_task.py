import pytest
from selenium import webdriver

ADMIN_LOGIN = "admin"
ADMIN_PASSWORD = "admin"

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

def test_login_into_admin(driver):
    driver.get("http://localhost/litecart/admin")
    assert "My Store" in driver.title
    login = driver.find_element_by_name("username")
    login.send_keys(ADMIN_LOGIN)
    password = driver.find_element_by_name("password")
    password.send_keys(ADMIN_PASSWORD)
    driver.find_element_by_name("login").click()