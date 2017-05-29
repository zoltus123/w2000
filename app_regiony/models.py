#-*- coding: utf-8 -*-

from django.db import models

# Create your models here.


class Wojewodztwo(models.Model):
    nazwa = models.CharField(max_length=500, unique=True)
    class Meta:
        verbose_name = "Województwo"
        verbose_name_plural = "Województwa"
        ordering = ('nazwa', )

    def __str__(self):
        return self.nazwa

class Powiat(models.Model):
    nazwa = models.CharField(max_length=500)
    wojewodztwo = models.ForeignKey('Wojewodztwo')
    class Meta:
        verbose_name = "Powiat"
        verbose_name_plural= "Powiaty"

    def __str__(self):
        return "%s (%s)" % (self.nazwa, self.wojewodztwo)

class Gmina(models.Model):
    nazwa = models.CharField(max_length=500)
    powiat = models.ForeignKey('Powiat', related_name='gminy')
    kod = models.PositiveIntegerField(unique=True)
    class Meta:
        verbose_name = "Gmina"
        verbose_name_plural= "Gminy"
    def __str__(self):
        return "%s (%s, %s)" % (self.nazwa, self.powiat.nazwa, self.powiat.wojewodztwo.nazwa)