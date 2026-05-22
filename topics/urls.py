from django.urls import path

from . import views

app_name = "topics"

urlpatterns = [
    path("", views.topic_index, name="index"),
    path("<slug:slug>/", views.topic_detail, name="detail"),
]
