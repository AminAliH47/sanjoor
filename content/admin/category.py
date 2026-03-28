from django.contrib import admin

from content.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = (
        'id',
        'text',
        'parent',
        'url',
        'poet',
    )
    list_display = (
        'text',
    )
    search_fields = (
        'text',
        'poet',
    )
