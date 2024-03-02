from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from .models import TaskGroup
from .views import GroupListView, GroupTaskListView, GroupUpdateView, GroupDeteleView
from .forms import CreateGroupForm, UpdateGroupForm
from todos.models import Task


class GroupTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            password="password"
        )

        cls.group = TaskGroup.objects.create(
            name="Test Group"
        )

        cls.task = Task.objects.create(
            user = cls.user,
            group = cls.group,
            title = "Test Task"
        )

        cls.group.members.add(cls.user)

    def test_group_list_view_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("groups:group_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.group.name)
        self.assertTemplateUsed(response, "groups/group_list.html")

    def test_group_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse("groups:group_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "%s?next=/group/" % (reverse("account_login"))
        )
        response = self.client.get("%s?next=/group/" % (reverse("account_login")))
        self.assertContains(response, "LogIn")

    def test_group_create_form(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("groups:group_list"))
        form = response.context["create_form"]
        self.assertIsInstance(form, CreateGroupForm)
        self.assertContains(response, "csrfmiddlewaretoken")
        self.assertEqual(TaskGroup.objects.all().count(), 1)

    def test_group_list_resolves_correct_view(self):
        view = resolve("/group/")
        self.assertEqual(view.func.__name__, GroupListView.as_view().__name__)

    def test_group_task_list_view_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("groups:group_task_list", args=[self.group.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.group.name)
        self.assertContains(response, self.task.title)
        self.assertTemplateUsed(response, "todos/task_list.html")

    def test_group_task_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse("groups:group_task_list", args=[self.group.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"%s?next=/group/{self.group.id}/tasks" % (reverse("account_login"))
        )
        response = self.client.get(f"%s?next=/group/{self.group.id}/tasks" % (reverse("account_login")))
        self.assertContains(response, "LogIn")
    
    def test_group_task_list_resolves_correct_view(self):
        view = resolve(f"/group/{self.group.id}/tasks")
        self.assertEqual(view.func.__name__, GroupTaskListView.as_view().__name__)

    def test_group_update_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("groups:group_update", args=[self.group.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "groups/group_update.html")
    
    def test_group_update_form(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("groups:group_update", args=[self.group.id]))
        form = response.context.get("form")
        self.assertIsInstance(form, UpdateGroupForm)
        self.assertContains(response, "csrfmiddlewaretoken")
    
    def test_group_update_resolves_correct_view(self):
        view = resolve(f"/group/{self.group.id}/update")
        self.assertEqual(view.func.__name__, GroupUpdateView.as_view().__name__)
    
    def test_group_delete_view(self):
        pass

