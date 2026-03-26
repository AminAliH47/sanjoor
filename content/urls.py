from django.urls import path

from content.views import (
    CategoryDetailView,
    HomeView,
    PoemDetailView,
    PoetDetailView,
    SearchView,
)

app_name = 'content'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('poets/<int:poet_id>/', PoetDetailView.as_view(), name='poet-detail'),
    path('categories/<int:category_id>/', CategoryDetailView.as_view(), name='category-detail'),
    path('poems/<int:poem_id>/', PoemDetailView.as_view(), name='poem-detail'),
]
