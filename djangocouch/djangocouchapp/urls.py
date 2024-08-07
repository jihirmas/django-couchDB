from django.urls import path
from djangocouchapp.views import author_views

author_urls = [
    path("create-author/", author_views.create_author, name='create_author'),
    path("", author_views.author_management, name='author_management'),
    path("<str:author_id>/",  author_views.view_author, name='view_author'),
    path("<str:author_id>/edit/",  author_views.edit_author, name='edit_author'),
    path("<str:author_id>/delete/",  author_views.delete_author, name='delete_author'),
    path("list-authors/", author_views.list_authors, name='list_authors'),
]

urlpatterns = [
    *author_urls
]
