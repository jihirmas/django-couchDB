from django.urls import path
from djangocouchapp.views import author_views, book_views, sales_views, tables_views, review_views

author_urls = [
    path("create-author/", author_views.create_author, name='create_author'),
    path("list-authors/", author_views.author_management, name='author_management'),
    path("<str:author_id>/edit/", author_views.edit_author, name='edit_author'),
    path("<str:author_id>/delete/", author_views.delete_author, name='delete_author'),
    path('authors/view/<str:author_id>/', author_views.view_author, name='view_author'),
    path("", author_views.author_management, name='author_management'),
]

book_urls = [
    path("create-book/", book_views.create_book, name='create_book'),
    path("view-book/<str:book_id>/", book_views.view_book, name='view_book'),
    path('list-books/', book_views.list_books, name="list_books"),
    path('book-management/', book_views.list_books, name='book_management'),
    path('book/<str:book_id>/edit/', book_views.edit_book, name='edit_book'),
    path('book/<str:book_id>/delete/', book_views.delete_book, name='delete_book'),
]

sales_urls = [
    path("create-sale/", sales_views.create_sale, name="create_sale"),
    path("edit-sale/<str:sale_id>/", sales_views.edit_sale, name="edit_sale"),
    path("list-sales/", sales_views.list_sales, name="list_sales"),
    path('sale/<str:sale_id>/delete/', sales_views.delete_sale, name='delete_sale'),
]

tables_urls = [
    path('top-50-books/',tables_views.top_50_books_view, name='top_50_books'),
    path('search_books/', tables_views.search_view, name="search_books"),
    path('top-10-rated-books/', tables_views.top_10_rated_books, name="top_10"),
    path('author-stats/', tables_views.author_statistics_view, name="author_stats")
]

review_urls = [
    path("create-review/", review_views.create_review, name='create_review'),
    path("edit-review/<str:review_id>/", review_views.edit_review, name='edit_review'),
    path("delete-review/<str:review_id>/", review_views.delete_review, name='delete_review'),
    path("view-review/<str:review_id>/", review_views.view_review, name='view_review'),
    path("list-reviews/", review_views.list_reviews, name='list_reviews'),
]



urlpatterns = [
    *author_urls,
    *book_urls,
    *sales_urls,
    *tables_urls,
    *review_urls,
]
