from django.urls import path

from . import views

app_name = "topics"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("search/", views.search, name="search"),
    path("submit/", views.submit, name="submit"),
    path("vote/<str:target>/<int:pk>/", views.vote, name="vote"),
    path("stance/<int:pk>/", views.stance, name="stance"),
    path("qlean/<int:pk>/", views.question_lean, name="question_lean"),
    path("respond/<int:pk>/", views.respond, name="respond"),
    path("category/<slug:slug>/", views.category_detail, name="category"),
    path("<slug:slug>/poster/", views.poster, name="poster"),
    path("<slug:slug>/share/", views.share_cards, name="share"),
    path("<slug:slug>/", views.topic_detail, name="detail"),
]
