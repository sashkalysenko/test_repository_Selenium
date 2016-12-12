import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


def get_new_window(old_windows_list, current_windows_list):
    """function takes 2 lists: with old windows and current ones. Returns new window"""
    for item in old_windows_list:
        try:
            current_windows_list.remove(item)
        except ValueError:
            continue
        return current_windows_list[0]


def test_links_are_opened_in_new_window(driver):
    admin_login(driver)

    driver.find_element_by_css_selector("a[href *= countries]").click()
    driver.find_element_by_css_selector("a.button[href *= edit_country]").click()

    links_in_new_page = driver.find_elements_by_css_selector("td#content tr a[target = '_blank']")
    original_window = driver.current_window_handle
    wait = WebDriverWait(driver, 10)

    for link in links_in_new_page:
        old_windows = driver.window_handles
        link.click()
        wait.until(EC.new_window_is_opened(old_windows))
        new_window = get_new_window(old_windows, driver.window_handles)
        driver.switch_to_window(new_window)
        driver.close()
        driver.switch_to_window(original_window)
