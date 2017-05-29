import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


driver = webdriver.Chrome()
driver.get('http://www.mimuw.edu.pl')

inp = driver.find_element_by_css_selector('#edit-search-block-form--2')
inp.send_keys('Ciebiera', Keys.RETURN)

wynik = driver.find_element_by_link_text('Krzysztof Ciebiera')
wynik.click()

wynik = driver.find_element_by_link_text('http://www.mimuw.edu.pl/~ciebie/')
wynik.click()
#ActionChains(driver).move_to_element('#edit-search-block-form--2').perform()

WebDriverWait(driver, ).until(expected_conditions.visibility_of_element_located(By.CSS_SELECTOR, '*__'))