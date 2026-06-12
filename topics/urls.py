from django.urls import path

from . import views

app_name = "topics"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("search/", views.search, name="search"),
    path("submit/", views.submit, name="submit"),
    path("vote/<str:target>/<int:pk>/", views.vote, name="vote"),
    path("category/<slug:slug>/", views.category_detail, name="category"),
    path("<slug:slug>/poster/", views.poster, name="poster"),
    path("<slug:slug>/share/", views.share_cards, name="share"),
    path("<slug:slug>/", views.topic_detail, name="detail"),
]
