import time
from django.contrib.auth.models import User
from django.test import TestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException

# Create your tests here.

from app_regiony.models import Wojewodztwo, Powiat, Gmina
from app_wybory.models import Okreg, Obwod, Statystyka, Kandydat, WynikKandydata, WynikStatystyki

def getDriver():
    driver = webdriver.Chrome()
    driver.get('localhost:8000/static/kraj.html')
    driver.implicitly_wait(3)
    return driver

def wyloguj(driver: webdriver.Chrome):
    try:
        driver.find_element_by_link_text('Wyloguj się')
    except NoSuchElementException:
        pass



def zaloguj(driver : webdriver.Chrome, login, haslo):
    wyloguj(driver)
    driver.find_element_by_link_text('Zaloguj się').click()
    driver.find_element_by_id('username').send_keys(login)
    driver.find_element_by_id('password').send_keys(haslo)
    driver.find_element_by_id('zaloguj').click()

    time.sleep(3)
    print(driver.find_element_by_id('komunikaty').text)

    time.sleep(3)

    if(driver.find_element_by_id('komunikaty').text == 'Pomyślnie zalogowano'):
        return True
    return False

class UzytkownikTestCase(TestCase):
    def test_logowania(self):
        print("Test logowania w przeglądarce")
        driver = getDriver()

        assert zaloguj(driver, 'a', 'a') == False
        assert zaloguj(driver, 'miki', 'miki2017') == True

    def test_edycji(self):
        print("Test edycji w przeglądarce")
        pass

    def test_wyszukiwarki(self):
        print("Test wyszukiwania w przeglądarce")
        pass

    def test_rownoleglosci(self):
        print("Test równoległego działania dwóch użytkowników w przeglądarce")
        pass
