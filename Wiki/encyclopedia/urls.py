from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>/", views.redirect, name='redirect'),
    path("search/", views.search, name='search'),
    path("searchresults/", views.search_results, name='searchresults'),
    path("createnew", views.createnew, name="createnew"),
    path("edit/<str:name>", views.edit, name="edit"),
    path("random/", views.random_page, name="random"), 
]
