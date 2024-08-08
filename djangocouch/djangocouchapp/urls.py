from django.urls import path
from djangocouchapp.views import author_views, book_views, review_views

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
    path('list-books/', book_views.list_books, name="list_books")
]

review_urls = [
    path("create-review/", review_views.create_review, name='create_review'),
    path("edit-review/<str:review_id>/", review_views.edit_review, name='edit_review'),
    path("delete-review/<str:review_id>/", review_views.delete_review, name='delete_review'),
    path("view-review/<str:review_id>/", review_views.view_review, name='view_review'),
]

urlpatterns = [
    *author_urls,
    *book_urls,
    *review_urls,
]
