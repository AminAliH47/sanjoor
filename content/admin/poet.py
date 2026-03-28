from django.contrib import admin

from content.models import Poet


@admin.register(Poet)
class PoetAdmin(admin.ModelAdmin):
    readonly_fields = (
        'id',
        'name',
        'category',
        'description',
    )
    ordering = ('name',)
    list_display = (
        'name',
        'is_selected',
    )
    list_display_links = (
        'name',
    )
    list_editable = (
        'is_selected',
    )
    list_filter = (
        'is_selected',
    )
    search_fields = (
        'name',
        'description',
    )
