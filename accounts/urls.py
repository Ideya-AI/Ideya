from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.MergeLoginView.as_view(), name="login"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password/", views.StyledPasswordChangeView.as_view(), name="password"),
    path("delete/", views.delete_account, name="delete"),
    path("", views.settings_view, name="settings"),
]
