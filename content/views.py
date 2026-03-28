from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from content import selectors
from content.models import Category, Poem, Poet


class HomeView(ListView):
    model = Poet
    template_name = 'content/home.html'
    context_object_name = 'poets'
    paginate_by = 24

    def get_queryset(self):
        return selectors.get_poets()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_poets'] = selectors.get_selected_poets()
        return context


class PoetListSearchAjaxView(View):
    """JSON list of poets for live search on the home page (name and description)."""

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        poets = []
        for poet in selectors.search_poets_by_name_or_description(query):
            poets.append(
                {
                    'id': poet.id,
                    'name': poet.name or str(poet.id),
                    'description': (poet.description or '')[:280],
                    'photo_url': poet.photo.url if poet.photo else None,
                    'detail_url': reverse('content:poet-detail', kwargs={'poet_id': poet.id}),
                }
            )
        return JsonResponse({'poets': poets, 'query': query})


class PoetDetailView(DetailView):
    model = Poet
    template_name = 'content/poet_detail.html'
    context_object_name = 'poet'
    pk_url_kwarg = 'poet_id'

    def get_object(self, queryset=None):
        return selectors.get_poet_by_id(self.kwargs['poet_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = selectors.get_poet_categories(self.object)
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'content/category_detail.html'
    context_object_name = 'category'
    pk_url_kwarg = 'category_id'
    poems_per_page = 50

    def get_object(self, queryset=None):
        return selectors.get_category_by_id(self.kwargs['category_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['children'] = selectors.get_category_children(self.object)

        poems_qs = selectors.get_category_poems_queryset(self.object)
        paginator = Paginator(poems_qs, self.poems_per_page)
        context['poems_page'] = paginator.get_page(self.request.GET.get('page'))

        return context


class PoemDetailView(DetailView):
    model = Poem
    template_name = 'content/poem_detail.html'
    context_object_name = 'poem'
    pk_url_kwarg = 'poem_id'

    def get_object(self, queryset=None):
        return selectors.get_poem_by_id(self.kwargs['poem_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        verses = selectors.get_poem_verses(self.object)
        context['verse_rows'], context['single_verses'] = self._build_verse_layout(verses)
        context['sounds'] = selectors.get_poem_sounds(self.object)
        return context

    @staticmethod
    def _build_verse_layout(verses):
        rows = []
        singles = []
        pending_right = None
        for verse in verses:
            if verse.position in (0, 2):
                if pending_right is not None:
                    singles.append(pending_right)
                pending_right = verse
                continue
            if verse.position in (1, 3):
                if pending_right is not None:
                    rows.append((pending_right, verse))
                    pending_right = None
                else:
                    singles.append(verse)
                continue
            if pending_right is not None:
                singles.append(pending_right)
                pending_right = None
            singles.append(verse)
        if pending_right is not None:
            singles.append(pending_right)
        return rows, singles


class SearchView(TemplateView):
    template_name = 'content/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        poems, verses = selectors.get_search_results(query=query, verse_limit=120)
        context['query'] = query
        context['poems'] = poems
        context['verses'] = verses
        return context
