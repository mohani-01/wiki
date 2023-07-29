from django.urls import path
from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="wiki"),
    path("wiki/<str:name>", views.page, name="page"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("edit/<str:file>", views.edit, name="edit"),
    path("random/", views.random, name="random"),
]
