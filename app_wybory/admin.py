from django.contrib import admin

# Register your models here.

from .models import Okreg, Obwod, Kandydat, Statystyka, WynikKandydata, WynikStatystyki

@admin.register(Okreg)
class OkrAdmin(admin.ModelAdmin):
    pass


@admin.register(Obwod)
class ObwAdmin(admin.ModelAdmin):
    pass


@admin.register(Kandydat)
class KandAdmin(admin.ModelAdmin):
    pass


@admin.register(Statystyka)
class StatAdmin(admin.ModelAdmin):
    pass


@admin.register(WynikKandydata)
class WynKandAdmin(admin.ModelAdmin):
    pass


@admin.register(WynikStatystyki)
class WynStatAdmin(admin.ModelAdmin):
    pass
