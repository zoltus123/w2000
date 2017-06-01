#-*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.

import locale
locale.setlocale(locale.LC_COLLATE, "pl_PL.UTF-8")

from .models import Wojewodztwo, Powiat, Gmina


@admin.register(Wojewodztwo)
class WojAdmin(admin.ModelAdmin):
    list_display = ('nazwa', )
    search_fields = ('nazwa', )


@admin.register(Powiat)
class PowAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'wojewodztwo_nazwa')
    list_filter = ('wojewodztwo',)
    search_fields = ('nazwa', 'wojewodztwo__nazwa')

    def wojewodztwo_nazwa(self, obj):
        return obj.wojewodztwo.nazwa
    wojewodztwo_nazwa.short_description = 'Województwo'
    wojewodztwo_nazwa.admin_order_field = 'wojewodztwo__nazwa'


@admin.register(Gmina)
class GmiAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'powiat_nazwa', 'wojewodztwo_nazwa', 'kod')
    list_filter = ('powiat__wojewodztwo',)
    search_fields = ('nazwa','powiat__nazwa', 'powiat__wojewodztwo__nazwa', 'kod')
    def wojewodztwo_nazwa(self, obj):
        return obj.powiat.wojewodztwo.nazwa
    wojewodztwo_nazwa.short_description = 'Województwo'
    wojewodztwo_nazwa.admin_order_field = 'powiat__wojewodztwo__nazwa'

    def powiat_nazwa(self, obj):
        return obj.powiat.nazwa
    powiat_nazwa.short_description = 'Powiat'
    powiat_nazwa.admin_order_field = 'powiat__nazwa'


