from django.urls import path
from djangocouchapp.views import author_views, book_views

author_urls = [
    path("create-author/", author_views.create_author, name='create_author'),
    path("", author_views.author_management, name='author_management'),
    path("<str:author_id>/edit/", author_views.edit_author, name='edit_author'),
    path("<str:author_id>/delete/", author_views.delete_author, name='delete_author'),
    path("list-authors/", author_views.list_authors, name='list_authors'),
]

book_urls = [
    path("create-book/", book_views.create_book, name='create_book'),
    path("view-book/<str:book_id>/", book_views.view_book, name='view_book'),
    path('list-books/', book_views.list_books, name="list_books"),
    path('book-management/', book_views.list_books, name='book_management'),
    path('book/<str:book_id>/edit/', book_views.edit_book, name='edit_book'),
    path('book/<str:book_id>/delete/', book_views.delete_book, name='delete_book'),
]


urlpatterns = [
    *author_urls,
    *book_urls,
]
