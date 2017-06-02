import time
from django.contrib.auth.models import User
from django.test import TestCase
import threading
from threading import Thread


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
    driver = webdriver.Firefox()
    driver.get('http://localhost:8000/static/kraj.html')
    driver.implicitly_wait(2)
    return driver


def brakEdycji(driver : webdriver.Firefox):
    try:
        assert not driver.find_element_by_link_text('Edytuj').is_displayed()
    except NoSuchElementException:
        pass


def wyloguj(driver: webdriver.Firefox):
    try:
        driver.find_element_by_link_text('Wyloguj się').click()
    except NoSuchElementException:
        pass
    driver.find_element_by_link_text('Zaloguj się')


def zaloguj(driver : webdriver.Firefox, login, haslo):
    wyloguj(driver)
    przycisk = driver.find_element_by_link_text('Zaloguj się')
    przycisk.click()

    poleLoginu = driver.find_element_by_id('username')
    poleLoginu.clear()
    poleLoginu.send_keys(login)

    poleHasla = driver.find_element_by_id('password')
    poleHasla.clear()
    poleHasla.send_keys(haslo)

    time.sleep(1)

    wyslij = driver.find_element_by_id('wyslij')
    wyslij.click()

    time.sleep(1)

    komunikat = driver.find_element_by_id('komunikaty').text

    if(komunikat == 'Pomyślnie zalogowano'):
        return True
    return False


def edytuj(driver : webdriver.Firefox, nrKand, wynik):
    nrKand += 1

    krajPrzed = int(driver.find_element_by_css_selector('#wyniki_tabelka tr:nth-child(' + str(nrKand) +
                                                        ') td:nth-child(3)').text)
    driver.find_element_by_link_text('Mazowieckie').click()
    wojPrzed = int(driver.find_element_by_css_selector('#wyniki_tabelka tr:nth-child(' + str(nrKand) +
                                                        ') td:nth-child(3)').text)
    driver.find_element_by_link_text('warszawski').click()
    powPrzed = int(driver.find_element_by_css_selector('#wyniki_tabelka tr:nth-child(' + str(nrKand) +
                                                       ') td:nth-child(3)').text)
    driver.find_element_by_link_text('Warszawa-Włochy').click()
    gmiPrzed = int(driver.find_element_by_css_selector('#wyniki_tabelka tr:nth-child(' + str(nrKand) +
                                                       ') td:nth-child(3)').text)
    driver.find_element_by_link_text('Obwód nr 7').click()
    obwPrzed = int(driver.find_element_by_css_selector('#wyniki_tabelka tr:nth-child(' + str(nrKand) +
                                                       ') td:nth-child(3)').text)

    roznica = wynik - obwPrzed

    driver.find_element_by_css_selector('#wyniki_tabelka tr:nth-child(' + str(nrKand) + ') a').click()
    driver.find_element_by_id('wynik').send_keys(wynik)
    driver.find_element_by_id('zapisz').click()
    driver.find_element_by_link_text('Powrót do strony głównej').click()
    krajPo = int(driver.find_element_by_css_selector('#wyniki_tabelka tr:nth-child(' + str(nrKand) +
                                                        ') td:nth-child(3)').text)
    driver.find_element_by_link_text('Mazowieckie').click()
    wojPo = int(driver.find_element_by_css_selector('#wyniki_tabelka tr:nth-child(' + str(nrKand) +
                                                       ') td:nth-child(3)').text)
    driver.find_element_by_link_text('warszawski').click()
    powPo = int(driver.find_element_by_css_selector('#wyniki_tabelka tr:nth-child(' + str(nrKand) +
                                                       ') td:nth-child(3)').text)
    driver.find_element_by_link_text('Warszawa-Włochy').click()
    gmiPo = int(driver.find_element_by_css_selector('#wyniki_tabelka tr:nth-child(' + str(nrKand) +
                                                       ') td:nth-child(3)').text)
    driver.find_element_by_link_text('Obwód nr 7').click()
    obwPo = int(driver.find_element_by_css_selector('#wyniki_tabelka tr:nth-child(' + str(nrKand) +
                                                       ') td:nth-child(3)').text)

    driver.find_element_by_link_text('Polska').click()

    if krajPo - krajPrzed != roznica:
        return False

    if wojPo - wojPrzed != roznica:
        return False

    if powPo - powPrzed != roznica:
        return False

    if gmiPo - gmiPrzed != roznica:
        return False

    if obwPo - obwPrzed != roznica:
        return False

    return True

class edytujThread(Thread):
    def __init__(self, driver: webdriver.Firefox, login, haslo, nrKand, wynik):
        Thread.__init__(self)
        self.driver = driver
        self.login = login
        self.haslo = haslo
        self.nrKand = nrKand
        self.wynik = wynik

    def run(self):
        zaloguj(self.driver, self.login, self.haslo)
        edytuj(self.driver, self.nrKand, self.wynik)
        self.driver.close()


class UzytkownikTestCase(TestCase):
    def test_braku_mozliwosci_edycji(self):
        print("Test braku możliwości edycji dla niezalogowanego użytkownika")
        driver = getDriver()
        brakEdycji(driver)
        driver.find_element_by_link_text('Mazowieckie').click()
        brakEdycji(driver)
        driver.find_element_by_link_text('warszawski').click()
        brakEdycji(driver)
        driver.find_element_by_link_text('Warszawa-Włochy').click()
        brakEdycji(driver)
        driver.find_element_by_link_text('Obwód nr 7').click()
        brakEdycji(driver)
        driver.close()


    def test_poprawnego_logowania_i_wylogowania(self):
        print("Test logowania w przeglądarce")
        driver = getDriver()
        assert zaloguj(driver, 'miki', 'miki2017') == True
        wyloguj(driver)
        driver.close()


    def test_niepoprawnego_logowania(self):
        print("Test niepoprawnego logowania w przeglądarce")
        driver = getDriver()
        assert zaloguj(driver, 'ab', 'ab') == False
        driver.close()


    def test_wyszukiwarki(self):
        print("Test wyszukiwania w przeglądarce")
        driver = getDriver()

        poleWyszukiwarki = driver.find_element_by_id('pole_wyszukiwarki')
        poleWyszukiwarki.send_keys('Bia')

        driver.find_element_by_link_text('Gmina Białystok (pow. Białystok)')

        try:
            driver.find_element_by_link_text('Gmina Warszawa-Włochy (pow. warszawski)')
            assert False
        except NoSuchElementException:
            pass

        driver.close()

    def test_edycji(self):
        print("Test edycji w przeglądarce")
        driver = getDriver()
        zaloguj(driver, 'miki', 'miki2017')
        assert edytuj(driver, 1, 0)
        driver.close()


    def test_watku(self):
        print("Test jednego wątku")

        driver = getDriver()
        zaloguj(driver, 'miki', 'miki2017')
        edytuj(driver, 1, 0)
        edytuj(driver, 2, 0)

        driver1 = getDriver()

        t = edytujThread(driver1, 'miki', 'miki2017', 1, 10)

        t.start()
        t.join()

        driver = getDriver()
        driver.find_element_by_link_text('Mazowieckie').click()
        driver.find_element_by_link_text('warszawski').click()
        driver.find_element_by_link_text('Warszawa-Włochy').click()
        driver.find_element_by_link_text('Obwód nr 7').click()

        wynik = int(driver.find_element_by_css_selector('#wyniki_tabelka tr:nth-child(2) td:nth-child(3)').text)
        assert wynik == 10
        driver.close()

    def test_rownoleglosci(self):
        print("Test równoległego działania dwóch użytkowników w przeglądarce")
        driver = getDriver()
        zaloguj(driver, 'miki', 'miki2017')
        edytuj(driver, 1, 0)
        edytuj(driver, 2, 0)
        wyloguj(driver)

        t1 = edytujThread(getDriver(), 'miki', 'miki2017', 1, 10)
        t2 = edytujThread(getDriver(), 'franek', 'papiez123', 2, 10)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        driver = getDriver()
        driver.find_element_by_link_text('Mazowieckie').click()
        driver.find_element_by_link_text('warszawski').click()
        driver.find_element_by_link_text('Warszawa-Włochy').click()
        driver.find_element_by_link_text('Obwód nr 7').click()

        wynik1 = int(driver.find_element_by_css_selector('#wyniki_tabelka tr:nth-child(2) td:nth-child(3)').text)
        wynik2 = int(driver.find_element_by_css_selector('#wyniki_tabelka tr:nth-child(3) td:nth-child(3)').text)
        assert  wynik1 + wynik2 == 10
        driver.close()
