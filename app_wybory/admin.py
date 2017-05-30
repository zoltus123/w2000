from django import forms
from django.contrib import admin

# Register your models here.
from django.core.exceptions import ValidationError

from .models import Obwod, Kandydat, Statystyka, WynikKandydata, WynikStatystyki


class wynKandObw(admin.TabularInline):
    model = WynikKandydata
    extra = 0
    readonly_fields = ('kandydat', 'obwod')


class wynStatObw(admin.TabularInline):
    model = WynikStatystyki
    extra = 0
    readonly_fields = ('statystyka', 'obwod')


@admin.register(Obwod)
class ObwAdmin(admin.ModelAdmin):
    list_display = ('numer', 'adres', 'gmina_nazwa', 'powiat_nazwa', 'wojewodztwo_nazwa')
    list_filter = ('gmina__powiat__wojewodztwo',)
    search_fields = ('numer', 'adres', 'gmina_nazwa', 'powiat_nazwa', 'wojewodztwo_nazwa')
    inlines = [
        wynKandObw, wynStatObw
    ]

    def wojewodztwo_nazwa(self, obj):
        return obj.gmina.powiat.wojewodztwo.nazwa
    wojewodztwo_nazwa.short_description = 'Województwo'
    wojewodztwo_nazwa.admin_order_field = 'gmina__powiat__wojewodztwo__nazwa'
    def powiat_nazwa(self, obj):
        return obj.gmina.powiat.nazwa
    powiat_nazwa.short_description = 'Powiat'
    powiat_nazwa.admin_order_field = 'gmina__powiat__nazwa'
    def gmina_nazwa(self, obj):
        return obj.gmina.nazwa
    gmina_nazwa.short_description = 'Gmina'
    gmina_nazwa.admin_order_field = 'gmina__nazwa'


@admin.register(Kandydat)
class KandAdmin(admin.ModelAdmin):
    list_display = ('nazwisko', 'imie')
    search_fields = ('imie', 'nazwisko')


@admin.register(Statystyka)
class StatAdmin(admin.ModelAdmin):
    list_display = ('nazwa', )
    search_fields = ('nazwa', )
