from django.urls import path

from .views import (
    ArticleListView, ArticleUpdateView,
    ArticleDeleteView, ArticleCreateView, article_detail_view
)

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('new/', ArticleCreateView.as_view(), name='article_new'),
    path('<slug:slug>/edit/', ArticleUpdateView.as_view(), name='article-edit'),
    path('<slug:slug>/', article_detail_view, name='article-detail'),
    path('<slug:slug>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
]
