from django.contrib import admin

# Register your models here.

from .models import Wojewodztwo, Powiat, Gmina


@admin.register(Wojewodztwo)
class WojAdmin(admin.ModelAdmin):
        pass

@admin.register(Powiat)
class PowAdmin(admin.ModelAdmin):
        pass

@admin.register(Gmina)
class GmiAdmin(admin.ModelAdmin):
        pass
