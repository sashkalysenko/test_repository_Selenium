import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

EMAIL = "Aerton@gmail.com"
PASSWORD = "password01"

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def test_new_user_registry(driver):
    driver.get("http://localhost/litecart/")
    driver.find_element_by_css_selector("a[href*=create_account").click()

    first_name = driver.find_element_by_css_selector("input[name=firstname]")
    first_name.send_keys("Aerton")

    last_name = driver.find_element_by_css_selector("input[name=lastname]")
    last_name.send_keys("Senna")

    address_one = driver.find_element_by_css_selector("input[name=address1]")
    address_one.send_keys("Street 1")

    post_code = driver.find_element_by_css_selector("input[name=postcode]")
    post_code.send_keys("K2G 6P9")

    city = driver.find_element_by_css_selector("input[name=city]")
    city.send_keys("Ontario")

    # country
    driver.find_element_by_css_selector("span.select2-selection__arrow").click()
    country = driver.find_element_by_css_selector("input.select2-search__field[type=search]")
    country.send_keys("canada" + Keys.ENTER)

    # zone_code
    driver.find_element_by_css_selector("select[name=zone_code]").click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "option[value=ON]")))
    driver.find_element_by_css_selector("option[value=ON]").click()

    email = driver.find_element_by_css_selector("input[type=email]")
    email.send_keys(EMAIL)

    phone = driver.find_element_by_css_selector("input[type=tel]")
    phone.send_keys("+380486523498")

    password = driver.find_element_by_css_selector("input[name=password]")
    password.send_keys(PASSWORD)
    confirmed_password = driver.find_element_by_css_selector("input[name=confirmed_password]")
    confirmed_password.send_keys(PASSWORD)
    # create account
    driver.find_element_by_css_selector("button[name=create_account").click()

    # log out
    driver.find_element_by_css_selector("a[href*=logout]").click()

    # log on
    driver.find_element_by_css_selector("input[name=email]").send_keys(EMAIL)
    driver.find_element_by_css_selector("input[name=password]").send_keys(PASSWORD)
    driver.find_element_by_css_selector("button[name=login]").click()


