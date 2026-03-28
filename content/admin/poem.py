from django.contrib import admin

from content.models import Poem, Verse


class VerseInline(admin.TabularInline):
    model = Verse
    ordering = ('order',)
    extra = 0
    can_delete = False
    readonly_fields = (
        'id',
        'order',
        'position',
        'text',
    )


@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    readonly_fields = (
        'id',
        'title',
        'category',
        'url',
    )
    inlines = (VerseInline,)
    list_display = (
        'title',
    )
    search_fields = (
        'title',
        'category',
    )
