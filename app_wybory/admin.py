from django import forms
from django.contrib import admin

# Register your models here.
from django.core.exceptions import ValidationError

from app_wybory.views import edytujWynik
from .models import Obwod, Kandydat, Statystyka, WynikKandydata, WynikStatystyki

class WynKandInline(admin.TabularInline):
    model = WynikKandydata
    extra = 0
    readonly_fields = ('kandydat', 'obwod', 'wynik')
    show_change_link = True

class WynStatInline(admin.TabularInline):
    model = WynikStatystyki
    extra = 0
    readonly_fields = ('statystyka', 'obwod', 'wynik')

@admin.register(Obwod)
class ObwAdmin(admin.ModelAdmin):
    list_display = ('numer', 'adres', 'gmina_nazwa', 'powiat_nazwa', 'wojewodztwo_nazwa')
    list_filter = ('gmina__powiat__wojewodztwo',)
    search_fields = ('numer', 'adres', 'gmina__nazwa', 'gmina__powiat__nazwa', 'gmina__powiat__wojewodztwo__nazwa')
    inlines = [
        WynKandInline, WynStatInline
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


@admin.register(WynikKandydata)
class WynKandAdmin(admin.ModelAdmin):
    list_display = ('obwod', 'kandydat', 'wynik')
    search_fields = ('obwod__numer','obwod__adres', 'kandydat__imie', 'kandydat__nazwisko')

