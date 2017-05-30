#-*- coding: utf-8 -*-

from django.db import models

# Create your models here.


class Okreg(models.Model):
    numer = models.PositiveIntegerField(unique=True)
    wojewodztwo = models.ForeignKey('regiony.Wojewodztwo')
    class Meta:
        verbose_name = "Okręg"
        verbose_name_plural="Okręgi"
    def __str__(self):
        return "Okręg nr " + str(self.numer)


class Obwod(models.Model):
    numer = models.PositiveIntegerField()
    gmina = models.ForeignKey('regiony.Gmina')
    okreg = models.ForeignKey('Okreg')
    adres = models.CharField(max_length=1000)
    typ = models.CharField(max_length=1)
    class Meta:
        verbose_name = "Obwód"
        verbose_name_plural="Obwody"
    def __str__(self):
        return "Obwód nr " + str(self.numer) + " " + self.adres


class Kandydat(models.Model):
    imie = models.CharField(max_length=42)
    nazwisko = models.CharField(max_length=200)
    class Meta:
        verbose_name = "Kandydat"
        verbose_name_plural="Kandydaci"

    def __str__(self):
        return self.imie + " " + self.nazwisko


class Statystyka(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name = "Statystyka"
        verbose_name_plural="Statystyki"

    def __str__(self):
        return self.nazwa


class WynikKandydata(models.Model):
    kandydat = models.ForeignKey('Kandydat')
    obwod = models.ForeignKey('Obwod')
    wynik = models.PositiveIntegerField()
    class Meta:
        unique_together=('kandydat', 'obwod')
        verbose_name = "Wynik kandydata w obwodzie"
        verbose_name_plural="Wyniki kandydatów w obwodach"

    def __str__(self):
        return "Wynik kandydata"

class WynikStatystyki(models.Model):
    statystyka = models.ForeignKey('Statystyka')
    obwod = models.ForeignKey('Obwod')
    wynik = models.PositiveIntegerField()
    class Meta:
        unique_together=('statystyka', 'obwod')
        verbose_name = "Wynik statystyki"
        verbose_name_plural="Wyniki statystyk"

    def __str__(self):
        return "Wynik statystyki"