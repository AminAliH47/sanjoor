from django.db.models import Q, QuerySet

from audio.models import PoemSound
from content.models import Category, Poem, Poet, Verse


def get_empty_poem_queryset() -> QuerySet[Poem]:
    return Poem.objects.none()


def get_empty_verse_queryset() -> QuerySet[Verse]:
    return Verse.objects.none()


def get_poets() -> QuerySet[Poet]:
    return Poet.objects.order_by('name')


def get_poet_by_id(poet_id: int) -> Poet:
    return Poet.objects.get(pk=poet_id)


def get_poet_categories(poet: Poet) -> QuerySet[Category]:
    return Category.objects.filter(poet_id=poet.id).order_by('id')


def get_category_by_id(category_id: int) -> Category:
    return Category.objects.get(pk=category_id)


def get_category_children(category: Category) -> QuerySet[Category]:
    return Category.objects.filter(parent_id=category.id).order_by('id')


def get_category_poems(category: Category) -> QuerySet[Poem]:
    return Poem.objects.filter(category_id=category.id).order_by('id')


def get_poem_by_id(poem_id: int) -> Poem:
    return Poem.objects.get(pk=poem_id)


def get_poem_verses(poem: Poem) -> QuerySet[Verse]:
    return Verse.objects.filter(poem_id=poem.id).order_by('order')


def get_poem_sounds(poem: Poem) -> QuerySet[PoemSound]:
    return PoemSound.objects.filter(poem_id=poem.id).order_by('id')


def search_poems_and_verses(query: str) -> tuple[QuerySet[Poem], QuerySet[Verse]]:
    poems = Poem.objects.filter(Q(title__icontains=query) | Q(url__icontains=query)).order_by('id')
    verses = Verse.objects.filter(text__icontains=query).select_related('poem').order_by('poem_id', 'order')
    return poems, verses


def get_search_results(query: str, verse_limit: int = 120) -> tuple[QuerySet[Poem], QuerySet[Verse]]:
    if not query:
        return get_empty_poem_queryset(), get_empty_verse_queryset()
    poems, verses = search_poems_and_verses(query)
    return poems, verses[:verse_limit]
