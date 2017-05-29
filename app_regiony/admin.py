from django.contrib import admin

# Register your models here.

from .models import Wojewodztwo, Powiat, Gmina

class skalaPowiatu(admin.SimpleListFilter):
        title = "Skala powiatu"
        parameter_name = "sk_pow"
        def lookups(self, request, model_admin):
                return (("m","mały"),("d","duży"))

        def queryset(self, request, queryset):
                v = self.value()
                if v == 'd' :
                        return queryset.filter(gmina_set__count__gt=10)
                if v == 'm' :
                        return queryset.filter(gmina_set__count__lt=10)
                return queryset

class GminyWPowiecie(admin.TabularInline):
        model = Gmina
        extra = 1

@admin.register(Wojewodztwo)
class WojAdmin(admin.ModelAdmin):
        pass

@admin.register(Powiat)
class PowAdmin(admin.ModelAdmin):
        list_display = ('nazwa', 'wojewodztwo', 'liczbaGmin')
        list_filter = ('wojewodztwo', skalaPowiatu)
        search_fields = ('nazwa', )
        inlines = (GminyWPowiecie, )

        def liczbaGmin(self, obj):
                return obj.gminy.count()

        liczbaGmin.short_description = "Liczba gmin"
        #liczbaGmin.admin_order_field = "gmina_set__count"

@admin.register(Gmina)
class GmiAdmin(admin.ModelAdmin):
        list_display = ('nazwa', 'powiat', 'kod')
