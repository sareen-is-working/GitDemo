# to run parallel tests import pytest-xdist and then run command pytest -n 2

import json
import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PageObjects.login import LoginPage
test_data_path = '../data/test_e2eTestFramework.json'
with open(test_data_path) as f:
    test_data = json.load(f)
    test_list = test_data["data"]

@pytest.mark.smoke
@pytest.mark.parametrize("test_list_item",test_list)
def test_e2e(browserInstance,test_list_item):
    driver = browserInstance
    driver.get("https://rahulshettyacademy.com/loginpagePractise/")
    loginpage = LoginPage(driver)
    print(loginpage.getTitle())
    shoppage = loginpage.login(test_list_item["userEmail"],test_list_item["userPassword"])
    shoppage.add_product_to_card(test_list_item['productName'])
    print(shoppage.getTitle())
    checkout_confirmation = shoppage.goToCart()
    checkout_confirmation.checkout()
    checkout_confirmation.enter_delivery_address("ind")
    checkout_confirmation.validate_order()