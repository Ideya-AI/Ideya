from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

from topics.models import Stance, Submission, Vote
from topics.participation import (
    merge_session_participation,
    retract_user_participation,
)

from .forms import LoginForm, SignUpForm


class MergeLoginView(LoginView):
    """Login that absorbs the anonymous session's participation. The key is
    captured before authentication because login() cycles it."""

    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        anon_key = self.request.session.session_key
        response = super().form_valid(form)
        merge_session_participation(self.request.user, anon_key)
        return response


class SignUpView(CreateView):
    template_name = "accounts/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("topics:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("accounts:settings")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        anon_key = self.request.session.session_key
        login(self.request, self.object)
        merge_session_participation(self.object, anon_key)
        return response


class StyledPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:settings")

    def form_valid(self, form):
        messages.success(self.request, "Password changed.")
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for f in form.fields.values():
            f.widget.attrs.update({"class": "field"})
        return form


@login_required
def settings_view(request):
    user = request.user
    return render(
        request,
        "accounts/settings.html",
        {
            "participation": {
                "votes": Vote.objects.filter(user=user).count(),
                "stances": Stance.objects.filter(user=user).count(),
                "submissions": Submission.objects.filter(user=user).count(),
            }
        },
    )


@login_required
@require_POST
def delete_account(request):
    """Remove the account and its personal signals. Vote counters are undone
    first; submissions stay as anonymized aggregate content (user SET_NULL)."""
    user = request.user
    retract_user_participation(user)
    logout(request)
    user.delete()
    messages.success(request, "Your account and participation are deleted.")
    return redirect("topics:home")
