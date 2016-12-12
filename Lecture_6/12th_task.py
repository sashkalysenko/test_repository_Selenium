import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

NEW_PRODUCT_NAME = "Kitty"


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


def new_product_creation(driver):
    # login and navigate to creation new product page
    admin_login(driver)
    driver.find_element_by_css_selector("a[href *= catalog]").click()
    driver.find_element_by_css_selector("a[href *= edit_product]").click()

    # General
    driver.find_element_by_css_selector("input[type=radio][value='1']").click()
    driver.find_element_by_css_selector("input[name='name[en]']").send_keys(NEW_PRODUCT_NAME)
    driver.find_element_by_css_selector("input[name='code']").send_keys("k001")
    driver.find_element_by_css_selector("input[type=checkbox][value='1-3']").click()
    quantity = driver.find_element_by_css_selector("input[name='quantity']")
    quantity.clear()
    quantity.send_keys("5,00")
    driver.find_element_by_css_selector("input[name='date_valid_from']").send_keys("01122016")
    driver.find_element_by_css_selector("input[name='date_valid_to']").send_keys("31122016")

    # Information
    driver.find_element_by_css_selector("a[href='#tab-information']").click()
    driver.find_element_by_css_selector("input[name='keywords']").send_keys("test")
    driver.find_element_by_css_selector("input[name='short_description[en]']").send_keys("test")
    driver.find_element_by_css_selector("div[class='trumbowyg-editor']").send_keys("test")
    driver.find_element_by_css_selector("input[name='head_title[en]']").send_keys("test")
    driver.find_element_by_css_selector("input[name='meta_description[en]']").send_keys("test")

    # Prices
    driver.find_element_by_css_selector("a[href='#tab-prices']").click()
    purchase_price = driver.find_element_by_css_selector("input[name='purchase_price']")
    purchase_price.clear()
    purchase_price.send_keys("18,99")
    select = Select(driver.find_element_by_css_selector("select[name='purchase_price_currency_code']"))
    select.select_by_visible_text("US Dollars")
    driver.find_element_by_css_selector("input[name='prices[USD]']").send_keys("18.99")
    gross_prices_eur = driver.find_element_by_css_selector("input[name='gross_prices[EUR]']")
    gross_prices_eur.clear()
    gross_prices_eur.send_keys("15")

    # Saving a product
    driver.find_element_by_css_selector("button[name='save']").click()


def test_verify_created_product(driver):
    new_product_creation(driver)
    products = driver.find_elements_by_css_selector("table.dataTable tr.row")
    list_of_products = []
    for product in products:
        product_name = str(product.find_element_by_css_selector("a").get_attribute("textContent"))
        list_of_products.append(product_name)
    assert NEW_PRODUCT_NAME in list_of_products
