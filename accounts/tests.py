from django.test import TestCase
from django.urls import reverse, resolve
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model

from .views import CustomUserSignupView


class SignupPageTests(TestCase):
    username = "newuser"
    email = "newuser@email.com"

    def setUp(self):
        url = reverse("account_signup")
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "account/signup.html")
        self.assertContains(self.response, "Sign Up")
        self.assertNotContains(self.response, "I'm not here")

    def test_signup_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, SignupForm)
        self.assertContains(self.response, "csrfmiddlewaretoken")

        new_user = get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)

    def test_signup_view(self):
        view = resolve("/custom_accounts/signup/")
        self.assertEqual(view.func.__name__, CustomUserSignupView.as_view().__name__)
        