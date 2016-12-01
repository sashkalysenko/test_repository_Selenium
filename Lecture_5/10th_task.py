import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_correct_page_of_product(driver):
    driver.get("http://localhost/litecart")
    driver.find_element_by_css_selector("div#box-campaigns li").click()
    print('lalala')