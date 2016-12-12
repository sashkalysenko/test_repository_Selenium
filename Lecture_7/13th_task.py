import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def are_elements_present(driver, *args):
    return len(driver.find_elements(*args)) > 0


def test_work_with_cart(driver):
    driver.get("http://localhost/litecart")

    # adding 3 products to cart
    ammount_of_products = 3
    for product in range(1, ammount_of_products + 1):
        driver.find_element_by_css_selector("div#box-latest-products li:nth-of-type({0})".format(product)).click()
        if are_elements_present(driver, By.CSS_SELECTOR, "select[name='options[Size]']"):
            select = Select(driver.find_element_by_css_selector("select[name='options[Size]']"))
            select.select_by_visible_text("Small")
        driver.find_element_by_css_selector("button[name='add_cart_product']").click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div#cart-wrapper span.quantity"), str(product)))
        driver.find_element_by_css_selector("a[href='http://localhost/litecart/en/']").click()

    # moving all the products from cart
    driver.find_element_by_css_selector("a[href*='checkout']").click()
    for product in range(1, ammount_of_products + 1):
        driver.find_element_by_css_selector("div.viewport li").click()
        element = driver.find_element_by_css_selector("table[class = 'dataTable rounded-corners'] tr:not([class = header])")
        driver.find_element_by_css_selector("button[name = 'remove_cart_item']").click()
        wait.until(EC.staleness_of(element))
