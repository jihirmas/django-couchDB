from django.urls import path, re_path
from django.conf.urls import include
from djangocouchapp.views import author_views

author_urls = [
    path("create-author/", author_views.create_author)
]

urlpatterns = [
    *author_urls
]
