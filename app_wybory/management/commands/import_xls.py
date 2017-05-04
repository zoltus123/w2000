#-*- coding: utf-8 -*-

import glob
import os
import xlrd
import locale
from app_regiony.models import Wojewodztwo, Powiat, Gmina
from app_wybory.models import Okreg, Obwod, Kandydat, Statystyka, WynikKandydata, WynikStatystyki

from django.core.management.base import BaseCommand, CommandError

from pprint import pprint



locale.setlocale(locale.LC_COLLATE, "pl_PL.UTF-8")


"""Najpierw wczytujemy pliki xls do tablicy"""

dane = os.path.realpath("./dane")

LICZBA_OKREGOW = 68

STATYSTYKI = [
    "Uprawnieni",
    "Wydane karty",
    "Głosy oddane",
    "Głosy nieważne",
    "Głosy ważne"
]

KANDYDACI = [
    "Dariusz Maciej GRABOWSKI",
    "Piotr IKONOWICZ",
    "Jarosław KALINOWSKI",
    "Janusz KORWIN-MIKKE",
    "Marian KRZAKLEWSKI",
    "Aleksander KWAŚNIEWSKI",
    "Andrzej LEPPER",
    "Jan ŁOPUSZAŃSKI",
    "Andrzej Marian OLECHOWSKI",
    "Bogdan PAWŁOWSKI",
    "Lech WAŁĘSA",
    "Tadeusz Adam WILECKI"
]

WOJEWODZTWA = {
    "Dolnośląskie" : [1,2,3,4],
    "Kujawsko-Pomorskie" : [5,6,7],
    "Lubelskie" : [8,9,10,11,12],
    "Lubuskie" : [13,14],
    "Łódzkie" : [15,16,17,18,19],
    "Małopolskie" : [20,21,22,23,24,25,26,27],
    "Mazowieckie" : [28,29,30,31,32,33,34,35,36],
    "Opolskie" : [37,38],
    "Podkarpackie" : [39,40,41,42],
    "Podlaskie" : [43,44,45],
    "Pomorskie" : [46,47,48],
    "Śląskie": [49,50,51,52,53,54],
    "Świętokrzyskie": [55,56],
    "Warmińsko-Mazurskie" : [57,58,59],
    "Wielkopolskie" : [60,61,62,63,64],
    "Zachodniopomorskie" : [65,66,67,68]
}

"""
wiersz z tabelki:
nr okr, kod gminy, gmina, powiat, nr obw, typ obw, adres, uprawnieni, wydane karty, glosy oddane, glosy niewazne,
glosy wazne, Dariusz Maciej GRABOWSKI, Piotr IKONOWICZ, Jarosław Kalinowski, Janusz Korwin-Mikke, Marian KRZAKLEWSKI,
Aleksander KWAŚNIEWSKI, Andrzej LEPPER, Jan ŁOPUSZAŃSKI, Andrzej Marian OLECHOWSKI, Bogdan PAWŁOWSKI, Lech WAŁĘSA,
Tadeusz Adam WILECKI
"""

"""wczytywanie plików .xls
    format : wojewodztwa - > powiaty  ->   gminy ->  kod gminy
                                           gmina
                                           powiat
                                           obwody {}   -> nr obwodu
                                                          typ obwodu
                                                          adres
                                                          wyniki {} -> oddane głosy, Korwin itd.
"""





from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        print()
        path = os.path.join(settings.BASE_DIR, )
        wojewodztwa = {}
        for okregXLS in sorted(glob.glob(os.path.join(path, "dane", "obw*.xls"))):
            print("Processing: %s" % okregXLS)
            okregArkusz = xlrd.open_workbook(okregXLS).sheet_by_index(0)
            for i in range(1, okregArkusz.nrows):
                row = okregArkusz.row(i)
                """Znajdujemy województwo po okręgu"""
                woj = ""
                for w in WOJEWODZTWA:
                    if row[0].value in WOJEWODZTWA[w]:
                        woj = w
                        break
                wojewodztwa.setdefault(woj, {"powiaty": {}})

                """sprawdzamy, czy powiat już jest"""
                wojewodztwa[woj]["powiaty"].setdefault(row[3].value, {
                    "gminy": {}
                })
                """sprawdzamy, czy gmina jest już w powiecie"""
                wojewodztwa[woj]["powiaty"][row[3].value]["gminy"].setdefault(row[2].value, {
                    "kodGminy": int(row[1].value), "obwody": {}
                })
                """sprawdzamy, czy obwod jest już w gminie"""
                wojewodztwa[woj]["powiaty"][row[3].value]["gminy"][row[2].value]["obwody"].setdefault(
                    int(row[4].value), {
                    "typ": row[5].value, "adres": row[6].value, "okreg": int(row[0].value)
                })

                """dodajemy wyniki z obwodu"""
                wojewodztwa[woj]["powiaty"][row[3].value]["gminy"][row[2].value]["obwody"][row[4].value]["wyniki"] = {
                    "Uprawnieni": int(row[7].value),
                    "Wydane karty": int(row[8].value),
                    "Głosy oddane": int(row[9].value),
                    "Głosy nieważne": int(row[10].value),
                    "Głosy ważne": int(row[11].value),
                    "Dariusz Maciej GRABOWSKI": int(row[12].value),
                    "Piotr IKONOWICZ": int(row[13].value),
                    "Jarosław KALINOWSKI": int(row[14].value),
                    "Janusz KORWIN-MIKKE": int(row[15].value),
                    "Marian KRZAKLEWSKI": int(row[16].value),
                    "Aleksander KWAŚNIEWSKI": int(row[17].value),
                    "Andrzej LEPPER": int(row[18].value),
                    "Jan ŁOPUSZAŃSKI": int(row[19].value),
                    "Andrzej Marian OLECHOWSKI": int(row[20].value),
                    "Bogdan PAWŁOWSKI": int(row[21].value),
                    "Lech WAŁĘSA": int(row[22].value),
                    "Tadeusz Adam WILECKI": int(row[23].value)
                }
        print("woj: %s" % wojewodztwa)

        """Teraz wczytujemy do BD"""

        """Pomocnicze tablice z id"""
        woj_id = {}
        okr_id = {}
        kand_id = {}
        stat_id = {}

        """Wojewodztwa i okręgi"""
        for woj in WOJEWODZTWA:
            print("Do bazy: " + woj)
            woj_obj = Wojewodztwo(nazwa=woj)
            woj_obj.save()
            woj_id[woj] = woj_obj.id
            for okr in WOJEWODZTWA[woj]:
                print("Do bazy: " + str(okr))
                okr_obj = Okreg(numer=okr, wojewodztwo=woj_obj)
                okr_obj.save()
                okr_id[okr] = okr_obj.id

        """Kandydaci"""
        for kand in KANDYDACI:
            print("Do bazy: " + kand)
            slowa = kand.split()
            naz = slowa.pop()
            kand_obj = Kandydat(imie=(" ".join(slowa)), nazwisko=naz)
            kand_obj.save()
            kand_id[kand] = kand_obj.id

        """Statystyki"""
        for stat in STATYSTYKI:
            print("Do bazy: " + stat)
            stat_obj = Statystyka(nazwa=stat)
            stat_obj.save()
            stat_id[stat] = stat_obj.id

        i = 1
        for woj in wojewodztwa:
            print("WOJEWODZTWO NR %s" % i)
            i+=1
            j=1
            for pow in wojewodztwa[woj]["powiaty"]:
                print("POWIAT NR" + str(j))
                j+=1
                print("Do bazy: " + woj + " " + pow)
                pow_obj = Powiat(nazwa=pow, wojewodztwo_id=woj_id[woj])
                pow_obj.save()
                for gmina in wojewodztwa[woj]["powiaty"][pow]["gminy"]:
                    print("Do bazy: " + woj + " "+ pow + " " + gmina)
                    gmina_obj = Gmina(nazwa=gmina, powiat=pow_obj,
                            kod=wojewodztwa[woj]["powiaty"][pow]["gminy"][gmina]["kodGminy"])
                    gmina_obj.save()
                    for obw in wojewodztwa[woj]["powiaty"][pow]["gminy"][gmina]["obwody"]:
                        #print("Do bazy:" + woj + " " + pow + " " + gmina + " " + str(obw))
                        obw_obj = Obwod(numer=obw, gmina=gmina_obj,
                            adres=wojewodztwa[woj]["powiaty"][pow]["gminy"][gmina]["obwody"][obw]["adres"],
                            typ=wojewodztwa[woj]["powiaty"][pow]["gminy"][gmina]["obwody"][obw]["typ"],
                            okreg_id=okr_id[wojewodztwa[woj]["powiaty"][pow]["gminy"][gmina]["obwody"][obw]["okreg"]]
                         )
                        obw_obj.save()
                        for kand in KANDYDACI:
                            #print(kand + " " + str(obw))
                            wynik_kand_obj = WynikKandydata(kandydat_id=kand_id[kand],
                                obwod=obw_obj,
                                wynik=wojewodztwa[woj]["powiaty"][pow]["gminy"][gmina]["obwody"][obw]["wyniki"][kand])
                            wynik_kand_obj.save()

                        for stat in STATYSTYKI:
                            #print(stat + " " + str(obw))
                            wynik_stat_obj = WynikStatystyki(statystyka_id=stat_id[stat],
                                obwod=obw_obj,
                                wynik=wojewodztwa[woj]["powiaty"][pow]["gminy"][gmina]["obwody"][obw]["wyniki"][stat])
                            wynik_stat_obj.save()
if False:










        """






        """
