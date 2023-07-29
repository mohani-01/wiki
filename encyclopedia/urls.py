from django.urls import path
from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="wiki"),
    path("wiki/<str:name>", views.find, name="find"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("random/", views.randomm, name="random"),
    path("edit/<str:file>", views.edit, name="edit"),
]
