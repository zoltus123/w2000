#-*- coding: utf-8 -*-
# Create your views here.
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from app_regiony.models import *
from app_wybory.models import *

from .forms import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect

import locale
locale.setlocale(locale.LC_COLLATE, "pl_PL.UTF-8")

def dajWojewodztwa():
    return sorted([ {'nazwa':woj.nazwa, 'id': woj.id} for woj in Wojewodztwo.objects.all()], key=lambda woj:
        locale.strxfrm(woj['nazwa']))


def dajIdWojewodztw():
    return [woj.id for woj in Wojewodztwo.objects.all()]


def dajNazwyStatystyk():
    return sorted([stat.nazwa for stat in Statystyka.objects.all()])


def dajKandydatow():
    return sorted([{'id':kand.id, 'nazwisko':kand.nazwisko, 'imie':kand.imie} for kand in Kandydat.objects.all()],
                  key=lambda kand: locale.strxfrm(kand['nazwisko']))


def dajIdKandydatow():
    return [kand.id for kand in Kandydat.objects.all()]


def dajPowiaty(woj_id):
    return sorted([{'id': powiat.id, 'nazwa':powiat.nazwa} for powiat in Powiat.objects.filter(wojewodztwo__id=woj_id)],
                  key=lambda powiat: locale.strxfrm(powiat['nazwa']))


def dajGminy(pow_id):
    return sorted([{'id': gmina.id, 'nazwa': gmina.nazwa} for gmina in Gmina.objects.filter(powiat__id=pow_id)],
                  key=lambda gmina: locale.strxfrm(gmina['nazwa']))


def dajObwody(gmi_id):
    return sorted([{'id': obwod.id, 'numer': obwod.numer, 'adres': obwod.adres} for obwod in Obwod.objects.filter(
        gmina__id=gmi_id)], key=lambda obwod: obwod['numer'])

"""Generowanie wyników na poszczególnych szczeblach"""


def podajWynikiObwodu(obw_id):
    obwWyniki = {}
    for stat in dajNazwyStatystyk():
        obwWyniki[stat] = WynikStatystyki.objects.filter(statystyka__nazwa=stat, obwod__id=obw_id
                                    ).aggregate(Sum('wynik'))['wynik__sum']
    for kand in dajIdKandydatow():
        obwWyniki[kand] = WynikKandydata.objects.filter(kandydat_id=kand, obwod__id=obw_id
                                    ).aggregate(Sum('wynik'))['wynik__sum']
    return obwWyniki


def podajWynikiGminy(gmi_id):
    gmWyniki={}

    for stat in dajNazwyStatystyk():
        gmWyniki[stat] = WynikStatystyki.objects.filter(statystyka__nazwa=stat, obwod__gmina__id=gmi_id,
        ).aggregate(Sum('wynik'))['wynik__sum']
    for kand in dajIdKandydatow():
        gmWyniki[kand] = WynikKandydata.objects.filter(kandydat__id=kand,
         obwod__gmina__id=gmi_id).aggregate(Sum('wynik'))['wynik__sum']
    return gmWyniki


def podajWynikiPowiatu(pow_id):
    powWyniki = {}
    for stat in dajNazwyStatystyk():
        powWyniki[stat] = WynikStatystyki.objects.filter(statystyka__nazwa=stat, obwod__gmina__powiat__id=pow_id
                        ).aggregate(Sum('wynik'))['wynik__sum']
    for kand in dajIdKandydatow():
        powWyniki[kand] = WynikKandydata.objects.filter(kandydat__id=kand,
                 obwod__gmina__powiat__id=pow_id).aggregate(Sum('wynik'))['wynik__sum']
    return powWyniki


def podajWynikiWojewodztwa(woj_id):
    wojWyniki = {}
    for stat in dajNazwyStatystyk():
        wojWyniki[stat] = WynikStatystyki.objects.filter(statystyka__nazwa=stat,
             obwod__gmina__powiat__wojewodztwo__id=woj_id).aggregate(Sum('wynik'))['wynik__sum']
    for kand in dajIdKandydatow():
        wojWyniki[kand] = WynikKandydata.objects.filter(kandydat__id=kand,
             obwod__gmina__powiat__wojewodztwo__id=woj_id).aggregate(Sum('wynik'))['wynik__sum']
    return wojWyniki


def podajWynikiKraju():
    krajWyniki = {}

    for stat in dajNazwyStatystyk():
        krajWyniki[stat] = WynikStatystyki.objects.filter(statystyka__nazwa=stat).aggregate(Sum('wynik'))['wynik__sum']
    for kand in dajIdKandydatow():
        krajWyniki[kand] = WynikKandydata.objects.filter(kandydat__id=kand).aggregate(Sum('wynik'))['wynik__sum']

    return krajWyniki


def podajProcentoweWyniki(wyniki):
    procenty = {}

    for kandydat in dajIdKandydatow():
        try:
            procenty[kandydat] = float("{0:.2f}".format(100 * wyniki[kandydat]
                            / wyniki["Głosy ważne"]))
        except ZeroDivisionError:
            procenty[kandydat] = 0


    return procenty


def podajPozycje(wyniki):
    pozycje = {}
    pierwszy = 0
    drugi = 0
    for kandydat in dajIdKandydatow():
        if(wyniki[kandydat] > pierwszy):
            drugi = pierwszy
            pierwszy = wyniki[kandydat]
        elif(wyniki[kandydat] > drugi):
            drugi = wyniki[kandydat]
    for kandydat in dajIdKandydatow():
        if(wyniki[kandydat] == pierwszy):
            pozycje[kandydat] = "pierwszy"
        elif(wyniki[kandydat] == drugi):
            pozycje[kandydat] = "drugi"
        else:
            pozycje[kandydat] = "pozostali"
    return pozycje


def podajFrekwencje(wyniki):
    try:
        return float("{0:.2f}".format(100 * wyniki["Wydane karty"]
                                      / wyniki["Uprawnieni"]))
    except ZeroDivisionError:
        return 0


def podajFrekwencjeWoj():
    frekwencjaWoj = {}

    for woj in dajIdWojewodztw():
        try:
            frekwencjaWoj[woj] = float("{0:.2f}".format(100 *
                WynikStatystyki.objects.filter(statystyka__nazwa="Wydane karty",
                obwod__gmina__powiat__wojewodztwo__id=woj).aggregate(Sum('wynik'))['wynik__sum']
                 / WynikStatystyki.objects.filter(statystyka__nazwa="Uprawnieni",
                 obwod__gmina__powiat__wojewodztwo__id=woj).aggregate(Sum('wynik'))['wynik__sum']
            ))
        except ZeroDivisionError:
            frekwencjaWoj[woj] = 0

    return frekwencjaWoj


def index2(request):
    if "liczba_odwiedzen" not in request.session:
        request.session["liczba_odwiedzen"] = 1
    else:
        request.session["liczba_odwiedzen"] += 1
    return HttpResponse(request.session["liczba_odwiedzen"])

from django.contrib.auth.decorators import login_required



def index(request):
    wyniki = podajWynikiKraju()

    data = {
          'wojewodztwa': dajWojewodztwa(),
          'statystyki': dajNazwyStatystyk(),
          'kandydaci': dajKandydatow(),
          'frekwencjaWoj': podajFrekwencjeWoj(),
          'wyniki': wyniki,
          'procenty': podajProcentoweWyniki(wyniki),
          'pozycje': podajPozycje(wyniki),
          'frekwencja': podajFrekwencje(wyniki)
         }
    return render(request, "kraj.html", data)



def wojewodztwoView(request, woj_id):
    wojewodztwo = get_object_or_404(Wojewodztwo, id=woj_id)

    wyniki = podajWynikiWojewodztwa(woj_id)
    data = {
          'wojewodztwo': wojewodztwo,
          'powiatyWWojewodztwie': dajPowiaty(woj_id),
          'statystyki': dajNazwyStatystyk(),
          'kandydaci': dajKandydatow(),
          'wyniki': wyniki,
          'procenty': podajProcentoweWyniki(wyniki),
          'pozycje': podajPozycje(wyniki),
          'frekwencja': podajFrekwencje(wyniki)
         }
    return render(request, "wojewodztwo.html", data)

def wojNazView(request, woj):
    wojewodztwo = get_object_or_404(Wojewodztwo, nazwa=woj)

    return wojewodztwoView(request, wojewodztwo.id)

def powiatView(request, pow_id):
    powiat = get_object_or_404(Powiat, id=pow_id)

    wyniki = podajWynikiPowiatu(pow_id)

    data = {
          'powiat': powiat,
          'gminyWPowiecie': dajGminy( pow_id),
          'statystyki': dajNazwyStatystyk(),
          'kandydaci': dajKandydatow(),
          'wyniki': wyniki,
          'procenty': podajProcentoweWyniki(wyniki),
          'pozycje': podajPozycje(wyniki),
          'frekwencja': podajFrekwencje(wyniki)
         }
    return render(request, "powiat.html", data)


def gminaView(request, gmi_id):
    gmina = get_object_or_404(Gmina, id=gmi_id)

    wyniki = podajWynikiGminy(gmi_id)

    data = {
          'gmina': gmina,
          'adresyObwodow': dajObwody(gmi_id),
          'statystyki': dajNazwyStatystyk(),
          'kandydaci': dajKandydatow(),
          'wyniki': wyniki,
          'procenty': podajProcentoweWyniki(wyniki),
          'pozycje': podajPozycje(wyniki),
          'frekwencja': podajFrekwencje(wyniki)
         }
    return render(request, "gmina.html", data)


def obwodView(request,  obw_id):
    obwod = get_object_or_404(Obwod, id=obw_id)

    wyniki = podajWynikiObwodu(obw_id)

    data = {
          'obwod': obwod,
          'statystyki': dajNazwyStatystyk(),
          'kandydaci': dajKandydatow(),
          'wyniki': wyniki,
          'procenty': podajProcentoweWyniki(wyniki),
          'pozycje': podajPozycje(wyniki),
          'frekwencja': podajFrekwencje(wyniki)
         }
    return render(request, "obwod.html", data)


def szukajView(request):
    data = {}
    data['form'] = GminyForm()
    data['komunikat'] = ""

    if request.method == 'POST':
        form = GminyForm(request.POST)
        if form.is_valid():
            wzorzec = form.cleaned_data['wzorzec']
            data['gminy'] = Gmina.objects.filter(nazwa__contains=wzorzec)
            data['komunikat'] = "(znaleziono " + str(len(data['gminy'])) + ")"
    return render(request, 'szukaj.html', data)



@csrf_protect
def loginView(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    data = {}
    data['form'] = loginForm()
    data['komunikat'] = ""
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                else:
                    return HttpResponseRedirect('/')
        data['komunikat'] = "Podane dane są nieprawidłowe"
    return render(request, 'login.html', data)


def logoutView(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
@transaction.atomic
def edytujView(request, obw_id, kand_id):
    data = {}

    data['obwod'] = get_object_or_404(Obwod, id=obw_id)
    data['kand'] = get_object_or_404(Kandydat, id=kand_id)
    data['form'] = wynikForm()
    data['komunikat'] = ""

    if request.method == 'POST':
        form = wynikForm(request.POST)
        if form.is_valid():
            wynik = form.cleaned_data['wynik']
            if wynik < 0:
                data['komunikat'] = "Podaj dodatni wynik"
                return render(request, 'edytuj.html', data)
            wynikKand, created = WynikKandydata.objects.get_or_create(obwod=data['obwod'], kandydat=data['kand'],
                                                        defaults={'wynik': 0})

            roznica = wynik - wynikKand.wynik

            glosyOddane, created = WynikStatystyki.objects.get_or_create(obwod=data['obwod'],
                                                        statystyka__nazwa='Głosy oddane', defaults={'wynik': 0})

            wydaneKarty, created = WynikStatystyki.objects.get_or_create(obwod=data['obwod'],
                                                        statystyka__nazwa='Wydane karty', defaults={'wynik': 0})

            if glosyOddane.wynik + roznica > wydaneKarty.wynik:
                data['komunikat'] = "Suma głosów oddanych nie może przekraczać liczby wydanych kart"
                return render(request, 'edytuj.html', data)

            glosyWazne, created = WynikStatystyki.objects.get_or_create(obwod=data['obwod'],
                                                                statystyka__nazwa='Głosy ważne', defaults={
                    'wynik': 0
                })

            wynikKand.wynik += roznica
            wynikKand.save()

            glosyWazne.wynik += roznica
            glosyWazne.save()

            glosyOddane.wynik += roznica
            glosyOddane.save()

            data['komunikat'] = "Zapisano liczbę głosów: " + str(wynik)
            return render(request, 'edytuj.html', data)
        data['komunikat'] = "Dane są niepoprawne"
    return render(request, 'edytuj.html', data)


