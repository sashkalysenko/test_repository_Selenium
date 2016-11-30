import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def admin_login(driver):
    """Does login into admin-page"""
    driver.get("http://localhost/litecart/admin")
    assert "My Store" in driver.title
    driver.find_element_by_css_selector("div#box-login [name = username]").send_keys("admin")
    driver.find_element_by_css_selector("div#box-login [name = password]").send_keys("admin")
    driver.find_element_by_css_selector("button[name = login]").click()


def test_alphabetical_order_counties(driver):
    driver.find_element_by_css_selector("")