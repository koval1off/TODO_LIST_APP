from django.urls import path
from .views import CustomUserSignupView, CustomChangePasswordView, CustomChangePasswordDoneView


urlpatterns = [
    path("signup/", CustomUserSignupView.as_view(), name="signup"),
    path("change-password/", CustomChangePasswordView.as_view(), name="change_password"),
    path("change-password/done", CustomChangePasswordDoneView.as_view(), name="password_change_done"),
]
