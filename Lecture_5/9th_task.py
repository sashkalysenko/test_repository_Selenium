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


def id_for_column(driver, column_name):
    """return id of column name or False"""
    header = driver.find_elements_by_css_selector("form[name = countries_form] tr.header th")
    header_id = 0
    for element in header:
        if element.text == column_name:
            return header_id
        else:
            header_id += 1
    return False


def test_alphabetical_order_counties(driver):
    # login and navigate to Countries-page
    admin_login(driver)
    driver.find_element_by_css_selector("a[href *= countries]").click()
    rows = driver.find_elements_by_css_selector("form[name = countries_form] tr.row")
    # get ides of needed columns
    column_id = id_for_column(driver, "ID")
    column_name_id = id_for_column(driver, "Name")
    column_zones_id = id_for_column(driver, "Zones")
    # list for all countries
    countries_list = []
    # list for countries with time zones > 1
    id_countries_with_zones = []

    # loop to fill lists which noted above
    for row in rows:
        cells = row.find_elements_by_css_selector("td")
        row_id = int(cells[column_id].text)
        countries_list.append(cells[column_name_id].text)
        amount_of_zones = int(cells[column_zones_id].text)
        if amount_of_zones > 1:
            id_countries_with_zones.append(row_id)

    # verify alphabetical order of all countries
    correct_order = countries_list[:]
    correct_order.sort()
    assert countries_list == correct_order




