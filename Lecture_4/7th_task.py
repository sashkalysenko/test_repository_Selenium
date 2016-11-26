import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


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


def are_elements_present(driver, *args):
    return len(driver.find_elements(*args)) > 0


def test_go_through_vertical_menu(driver):
    admin_login(driver)
    amount_parent_menues = len(driver.find_elements_by_css_selector("td#sidebar li#app-"))
    # main loop to go through each main menu (parent)
    for parent in range(1, amount_parent_menues + 1):
        main_menu = driver.find_element_by_css_selector("td#sidebar li#app-:nth-of-type({0})".format(parent))
        main_menu.click()
        assert are_elements_present(driver, By.CSS_SELECTOR, "h1") == True
        amount_children_menues = len(driver.find_elements_by_css_selector("li#app-.selected li"))
        non_selected_children_menues = len(driver.find_elements_by_css_selector("li#app-.selected li:not(.selected)"))
        # case when
        if non_selected_children_menues:
            for child in range(2, amount_children_menues + 1):
                optional_menu = driver.find_element_by_css_selector(
                    "li#app-.selected li:nth-of-type({0})".format(child))
                optional_menu.click()
                assert are_elements_present(driver, By.CSS_SELECTOR, "h1") == True
        else:
            assert are_elements_present(driver, By.CSS_SELECTOR, "h1") == True
