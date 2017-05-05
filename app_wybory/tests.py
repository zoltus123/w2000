import threading

from django.test import TestCase, Client
from django.contrib.auth.models import User
from app_wybory.models  import *
from app_regiony.models import *
from django.db.models import Sum
from threading import Thread
# Create your tests here.


#Na bazie SQLite nie da się przetestować współbieżności
class edytujThread(Thread):
    def __init__(self, obwod: Obwod, kandydat: Kandydat, wynik: int):
        threading.Thread.__init__(self)
        self.obwod = obwod
        self.kandydat = kandydat
        self.wynik = wynik

    def run(self):
        print("zgłasza się wątek " + self.name)
        c = Client()
        c.force_login(User.objects.get(username="adam"))
        c.post('/edytuj/' + str(self.obwod.id) + '/' + str(self.kandydat.id),
                                    {'wynik': str(self.wynik)})
        print("wątek " + self.name + " kończy działanie")

class EdycjaTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('adam', 'adam@adam@.pl', 'adam')

        maz = Wojewodztwo.objects.create(nazwa="Mazowieckie")
        okregWar = Okreg.objects.create(numer=1, wojewodztwo=maz)
        warszawa = Powiat.objects.create(nazwa="Warszawa", wojewodztwo=maz)
        wlochy = Gmina.objects.create(nazwa="Włochy", powiat=warszawa, kod=1)
        obw1 = Obwod.objects.create(gmina=wlochy, okreg=okregWar, numer=1, typ='A', adres="Ryżowa")

        stat_wazne = Statystyka.objects.create(nazwa="Głosy ważne")
        stat_niewazne =Statystyka.objects.create(nazwa="Głosy nieważne")
        stat_oddane = Statystyka.objects.create(nazwa="Głosy oddane")
        stat_upr = Statystyka.objects.create(nazwa="Uprawnieni")
        stat_wydane = Statystyka.objects.create(nazwa="Wydane karty")

        kand1 = Kandydat.objects.create(imie="Jan", nazwisko="Kowalski")
        kand2 = Kandydat.objects.create(imie="Anna", nazwisko="Kowalska")

        WynikStatystyki.objects.create(obwod=obw1, statystyka=stat_upr, wynik=100)
        WynikStatystyki.objects.create(obwod=obw1, statystyka=stat_wydane, wynik=80)
        WynikStatystyki.objects.create(obwod=obw1, statystyka=stat_oddane, wynik=20)
        WynikStatystyki.objects.create(obwod=obw1, statystyka=stat_wazne, wynik=10)
        WynikStatystyki.objects.create(obwod=obw1, statystyka=stat_niewazne, wynik=10)

        WynikKandydata.objects.create(obwod=obw1, kandydat=kand1, wynik=5)
        WynikKandydata.objects.create(obwod=obw1, kandydat=kand2, wynik=5)


    def test_edycja_bez_logowania(self):

        print("Test edycji bez logowania")
        c = Client()
        obwod = Obwod.objects.get(adres="Ryżowa")
        kand = Kandydat.objects.get(nazwisko="Kowalski")
        przed = WynikKandydata.objects.get(obwod=obwod, kandydat=kand).wynik

        c.post('/edytuj/' + str(obwod.id) + '/' + str(kand.id),
               {'wynik': przed + 1})

        wynik = WynikKandydata.objects.get(obwod=obwod, kandydat=kand)

        self.assertEqual(przed, wynik.wynik)

        wynik.wynik = przed
        wynik.save()


    def test_edycja_z_logowaniem(self):
        print("Test edycji z logowaniem")
        c = Client()
        obwod = Obwod.objects.get(adres="Ryżowa")
        kand = Kandydat.objects.get(nazwisko="Kowalski")
        przed = WynikKandydata.objects.get(obwod=obwod, kandydat=kand).wynik

        c.login(username="adam", password="adam")
        c.post('/edytuj/' + str(obwod.id) + '/' + str(kand.id),
               {'wynik': przed + 1})

        wynik = WynikKandydata.objects.get(obwod=obwod, kandydat=kand)

        self.assertEqual(przed + 1, wynik.wynik)

        wynik.wynik = przed
        wynik.save()

    def test_edycji_ujemna(self):
        print("Test wprowadzenia ujemnego wyniku")
        c = Client()
        obwod = Obwod.objects.get(adres="Ryżowa")
        kand = Kandydat.objects.get(nazwisko="Kowalski")
        przed = WynikKandydata.objects.get(obwod=obwod, kandydat=kand).wynik

        c.login(username="adam", password="adam")
        c.post('/edytuj/' + str(obwod.id) + '/' + str(kand.id),
               {'wynik': -100})

        wynik = WynikKandydata.objects.get(obwod=obwod, kandydat=kand)

        self.assertEqual(przed, wynik.wynik)

        wynik.wynik = przed
        wynik.save()

    def test_edycji_za_duza(self):
        print("Test wprowadzenia zbyt dużej liczby głosów")

        c = Client()
        obwod = Obwod.objects.get(adres="Ryżowa")
        kand = Kandydat.objects.get(nazwisko="Kowalski")
        przed = WynikKandydata.objects.get(obwod=obwod, kandydat=kand).wynik
        uprawnieni = WynikStatystyki.objects.get(obwod=obwod, statystyka=Statystyka.objects.get(
            nazwa="Uprawnieni")).wynik

        c.login(username="adam", password="adam")
        c.post('/edytuj/' + str(obwod.id) + '/' + str(kand.id),
               {'wynik': uprawnieni + 1})

        wynik = WynikKandydata.objects.get(obwod=obwod, kandydat=kand)

        self.assertEqual(przed, wynik.wynik)

        wynik.wynik = przed
        wynik.save()

    """   
    def test_wspolbieznosc(self):
        obwod = Obwod.objects.get(adres="Ryżowa")
        kand1 = Kandydat.objects.get(nazwisko="Kowalski")
        kand2 = Kandydat.objects.get(nazwisko="Kowalska")
        
        threads = []
        
        for i in range(3):
            threads.append(edytujThread(obwod, kand1, 20))
            threads.append(edytujThread(obwod, kand2, 20))

        assert(WynikStatystyki.objects.get(obwod=obwod, statystyka__nazwa="Głosy ważne") <=
               WynikStatystyki.objects.get(obwod=obwod, statystyka__nazwa="Wydane karty"))
    
    """