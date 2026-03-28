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
    )
    search_fields = (
        'name',
        'description',
    )
