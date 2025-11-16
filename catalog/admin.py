from .models import AdSlot
from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Resource, Section, ClickEvent

@admin.action(description="Exportar seleção para CSV")
def export_csv(modeladmin, request, queryset):
    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = 'attachment; filename="resources.csv"'
    writer = csv.writer(resp)
    writer.writerow(["id","section","title","locale","country","url","phone","address","is_official","is_active","sort_order","created_at","updated_at"])
    for r in queryset:
        writer.writerow([r.id, r.section, r.title, r.locale, r.country, r.url, r.phone, r.address, r.is_official, r.is_active, r.sort_order, r.created_at, r.updated_at])
    return resp

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display  = ("section","title","locale","country","is_official","is_active","sort_order","updated_at")
    list_filter   = ("section","locale","country","is_official","is_active")
    search_fields = ("title","description","url","phone","address")
    ordering      = ("section","sort_order","id")
    list_editable = ("sort_order","is_active")          # edição inline rápida
    list_per_page = 25
    actions = [export_csv]
    date_hierarchy = "updated_at"

@admin.register(ClickEvent)
class ClickEventAdmin(admin.ModelAdmin):
    list_display = ("id","link","locale","country","created_at")
    list_filter  = ("locale","country")
    search_fields= ("referrer","user_agent","link__title")
    date_hierarchy = "created_at"
    list_per_page = 50


@admin.register(AdSlot)
class AdSlotAdmin(admin.ModelAdmin):
    list_display = ("position","country","title","is_active","sort_order","updated_at")
    list_filter  = ("position","country","is_active")
    search_fields= ("title","target_url")
    list_editable= ("is_active","sort_order")
    ordering    = ("position","sort_order","id")



# from django.contrib import admin
# from .models import Resource, Section

# @admin.register(Resource)
# class ResourceAdmin(admin.ModelAdmin):
#     list_display  = ("section","title","locale","country","is_official","is_active","sort_order")
#     list_filter   = ("section","locale","country","is_official","is_active")
#     search_fields = ("title","description","url","phone","address")
#     ordering      = ("section","sort_order","id")
