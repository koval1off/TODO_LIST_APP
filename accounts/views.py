from django.urls import reverse_lazy
from django.contrib.auth import logout
from allauth.account.views import SignupView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

from .forms import CustomSignupForm


class CustomUserSignupView(SignupView):
    form_class = CustomSignupForm
    template_name = "registration/signup.html"

    def form_valid(self, form):
        return super(CustomUserSignupView, self).form_valid(form)
        
    def get_success_url(self):
        return reverse_lazy("account_email_verification_sent")


class CustomChangePasswordView(PasswordChangeView):
    template_name = "account/password_change.html"

    def get_success_url(self):
        return reverse_lazy("password_change_done")
    

class CustomChangePasswordDoneView(PasswordChangeDoneView):
    template_name = "account/password_change_done.html"

