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


def id_for_column(driver, table, column_name):
    """return id of column name or False"""
    header = driver.find_elements_by_css_selector(table + " tr.header th")
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
    countries_table = "form[name = countries_form]"
    column_code_id = id_for_column(driver, countries_table, "Code")
    column_name_id = id_for_column(driver, countries_table, "Name")
    column_zones_id = id_for_column(driver, countries_table, "Zones")
    # list for all countries
    countries_list = []
    # list for countries with time zones > 1
    country_code_with_zones = []

    # loop to fill lists which are noted above
    for row in rows:
        cells = row.find_elements_by_css_selector("td")
        countries_list.append(cells[column_name_id].get_attribute('textContent'))
        amount_of_zones = int(cells[column_zones_id].get_attribute('textContent'))
        if amount_of_zones > 1:
            country_code = cells[column_code_id].get_attribute('textContent')
            country_code_with_zones.append(country_code)

    # verify alphabetical order of all countries
    correct_order = countries_list[:]
    correct_order.sort()
    assert countries_list == correct_order

    # verify alphabetical order of time zones for each country which has them
    for country in country_code_with_zones:
        # navigate to country with timezones
        driver.find_element_by_css_selector("a[href*='country_code={0}']".format(country)).click()
        # define table with zones
        zones_table = "table#table-zones"
        # get rows from zones_table
        rows = driver.find_elements_by_css_selector(zones_table + " tr:not([class = header])")
        # get id of column Name
        zones_name_id = id_for_column(driver, zones_table, "Name")
        # list for zones
        zones_list = []
        # loop to fill zones_list from current country
        for row in rows:
            cells = row.find_elements_by_css_selector("td")
            zone_name = cells[zones_name_id].get_attribute('textContent')
            if zone_name:
                zones_list.append(zone_name)

        # verify alphabetical order of all zones
        correct_order = zones_list[:]
        correct_order.sort()
        assert zones_list == correct_order
        # come back to Countries menu
        driver.find_element_by_css_selector("span.button-set button[name = cancel]").click()


def test_alphabetical_order_geoZones(driver):
    # login and navigate to GeoZones-page
    admin_login(driver)
    driver.find_element_by_css_selector("a[href *= geo_zones]").click()
    zones_table = "table.dataTable"
    amount_rows = len(driver.find_elements_by_css_selector(zones_table + " tr.row"))
    for one in range(1, amount_rows + 1):
        zones_list = []
        # navigate to each country
        driver.find_element_by_css_selector("a[href*='geo_zone_id={0}']".format(one)).click()
        column_zone_id = id_for_column(driver, zones_table, "Zone")
        rows = driver.find_elements_by_css_selector(zones_table + " tr:not([class = header])")
        for row in rows:
            cells = row.find_elements_by_css_selector("td")
            if len(cells) < column_zone_id:
                continue
            zone_cell = cells[column_zone_id]
            selected_option = zone_cell.find_element_by_css_selector("[selected = selected]").get_attribute('textContent')
            zones_list.append(selected_option)

        # verify alphabetical order of all zones
        correct_order = zones_list[:]
        correct_order.sort()
        assert zones_list == correct_order
        # come back to Geo Zones menu
        driver.find_element_by_css_selector("span.button-set button[name = cancel]").click()
