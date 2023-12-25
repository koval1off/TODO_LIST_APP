from django.urls import reverse_lazy
from django.contrib.auth import logout, login
from allauth.account.forms import SignupForm
from allauth.account import views as allauth_views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView


class CustomUserSignupView(allauth_views.SignupView):
    form_class = SignupForm
    template_name = "registration/signup.html"

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("account_email_verification_sent")


class CustomChangePasswordView(PasswordChangeView):
    template_name = "registration/password_change.html"
    success_url = reverse_lazy("password_change_done")

    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)
        return response
    

class CustomChangePasswordDoneView(PasswordChangeDoneView):
    template_name = "registration/password_change_done.html"

