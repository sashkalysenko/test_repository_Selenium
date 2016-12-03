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

    # empty dictionary for all needed properties from Home-page
    home_page_properties = {}

    # getting all needed properties + pull them to dict
    first_element = driver.find_element_by_css_selector("div#box-campaigns li:nth-of-type(1)")

    home_page_properties["name_of_product"] = first_element.find_element_by_css_selector("div.name").get_attribute(
        "textContent")
    home_page_properties["regular_price_value"] = first_element.find_element_by_css_selector(
        "s.regular-price").get_attribute("textContent")
    home_page_properties["regular_price_tag_name"] = first_element.find_element_by_css_selector(
        "s.regular-price").get_attribute("tagName")
    home_page_properties["regular_price_class"] = first_element.find_element_by_css_selector(
        "s.regular-price").get_attribute("className")
    home_page_properties["campaign_price_value"] = first_element.find_element_by_css_selector(
        "strong.campaign-price").get_attribute("textContent")
    home_page_properties["campaign_price_tag_name"] = first_element.find_element_by_css_selector(
        "strong.campaign-price").get_attribute("tagName")
    home_page_properties["campaign_price_class"] = first_element.find_element_by_css_selector(
        "strong.campaign-price").get_attribute("className")

    # navigate to Yellow Duck product-page
    driver.find_element_by_css_selector("div#box-campaigns li:nth-of-type(1)").click()

    # check that a page of the product has been opened
    product_page_title = driver.find_element_by_css_selector("h1.title").get_attribute("textContent")
    assert product_page_title == home_page_properties.get("name_of_product")

    # empty dictionary for all needed properties from Home-page
    product_page_properties = {}

    # getting all needed properties + pull them to dict
    product_info = driver.find_element_by_css_selector("div.information")

    product_page_properties["name_of_product"] = product_page_title
    product_page_properties["regular_price_value"] = product_info.find_element_by_css_selector(
        "s.regular-price").get_attribute("textContent")
    product_page_properties["regular_price_tag_name"] = product_info.find_element_by_css_selector(
        "s.regular-price").get_attribute("tagName")
    product_page_properties["regular_price_class"] = product_info.find_element_by_css_selector(
        "s.regular-price").get_attribute("className")
    product_page_properties["campaign_price_value"] = product_info.find_element_by_css_selector(
        "strong.campaign-price").get_attribute("textContent")
    product_page_properties["campaign_price_tag_name"] = product_info.find_element_by_css_selector(
        "strong.campaign-price").get_attribute("tagName")
    product_page_properties["campaign_price_class"] = product_info.find_element_by_css_selector(
        "strong.campaign-price").get_attribute("className")

    # compare all the properties between home-page and product-page
    for key in home_page_properties.keys():
        assert home_page_properties.get(key) == product_page_properties.get(key)
