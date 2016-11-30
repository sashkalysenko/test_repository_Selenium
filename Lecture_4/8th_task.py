import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def are_elements_present(driver, *args):
    return len(driver.find_elements(*args)) > 0


def one_duck_one_sticker(driver, css_locator):
    """verifies that only one sticker is assigned per each duck in one block.\
    Input - css-locator as string."""
    amount_of_ducks = len(driver.find_elements_by_css_selector(css_locator + " li"))
    for duck in range(1, amount_of_ducks + 1):
        sticker = driver.find_elements_by_css_selector(css_locator + " li:nth-of-type({0}) div[class^=sticker]".format(duck))
        assert len(sticker) == 1


def test_box_most_popular(driver):
    driver.get("http://localhost/litecart")
    box_most_popular_locator = "div#box-most-popular"
    one_duck_one_sticker(driver, box_most_popular_locator)

    box_campaigns_locator = "div#box-campaigns"
    one_duck_one_sticker(driver, box_campaigns_locator)

    box_latest_products_locator = "div#box-latest-products"
    one_duck_one_sticker(driver, box_latest_products_locator)
