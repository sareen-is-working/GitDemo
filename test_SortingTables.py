import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def test_sort(browserInstance):
    driver = browserInstance
    driver.implicitly_wait(2)
    driver.get("https://rahulshettyacademy.com/seleniumPractise/#/offers")
    browserSortedVeggies = []
    driver.find_element(By.XPATH, "//span[text()='Veg/fruit name']").click()
    veggieWebElements = driver.find_elements(By.XPATH, "//tr/td[1]")
    for ele in veggieWebElements:
        browserSortedVeggies.append(ele.text)

    originalSortedVeggies = browserSortedVeggies.copy()

    browserSortedVeggies.sort()
    assert browserSortedVeggies == originalSortedVeggies