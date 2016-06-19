from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth import views
from django.contrib.auth import get_user_model
from app.models import WorkDay, Project
from app.forms import WorkDayForm, CreateAccountForm
from .utils import TimeTestUtils

class TestProjectsView(TestCase, TimeTestUtils):
    fixtures = ['app']

    def setUp(self):
        self.login()

    def test_fixtures(self):
        user = get_user_model().objects.get(username="chrxr")
        project = Project.objects.get(projectName="Digital Miscellanies Index")
        self.assertEqual(project.projectName, "Digital Miscellanies Index")
        self.assertEqual(user.username, "chrxr")

    def test_project_view(self):

        response = self.client.get(reverse('projects-view'))
        project_one = Project.objects.get(pk=1)
        projects = response.context['projects']

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('/app/viewprojects.html')
        self.assertIn(project_one.projectName, projects)
        self.assertNotIn("BLURGH", projects)

    def test_project_sort_user(self):
        # Check that view returns times for each project ordered by users first name
        response = self.client.get('/projects-view/?sort=user')
        times = WorkDay.objects.filter(project__projectName='Digital Miscellanies Index').order_by('user__first_name')
        view_projects = response.context['projects']
        first_user = view_projects['Digital Miscellanies Index']['times'][0].user

        self.assertEqual(response.status_code, 200)
        self.assertEqual(first_user, times.first().user)

    def test_project_sort_date(self):
        # Check that view returns times for each project ordered by date
        response = self.client.get('/projects-view/?sort=date')
        times = WorkDay.objects.filter(project__projectName='Digital Miscellanies Index').order_by('date')
        view_projects = response.context['projects']
        first_date = view_projects['Digital Miscellanies Index']['times'][0].date

        self.assertEqual(response.status_code, 200)
        self.assertEqual(first_date, times.first().date)

    def test_unauthenticated_redirect(self):
        self.client.logout()
        response = self.client.get(reverse('projects-view'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/projects-view/")


class TestUserView(TestCase, TimeTestUtils):
    fixtures = ['app']

    def setUp(self):
        self.login()

    def test_user_view(self):

        response = self.client.get(reverse('users-view'))
        users = response.context['users']
        users_in_context = []
        for user in users:
            users_in_context.append(user)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('/app/viewusers.html')
        # When user first / lastname is not entered, username is displayed
        self.assertContains(response, "test@email.com")
        # When user has first / lastname entered, full name is displayed
        self.assertContains(response, "Chris Rogers")
        self.assertNotIn("BLURGH", users_in_context)

    def test_user_sort_project(self):
        # Check that view returns times for each user ordered by project name
        response = self.client.get('/users-view/?sort=user')
        times = WorkDay.objects.filter(user__username='chrxr').order_by('project__projectName')
        view_users = response.context['users']

        for user in view_users:
            for key, value in user.items():
                if key == "Chris Rogers":
                    first_project_name = value['times'][0].project

        self.assertEqual(response.status_code, 200)
        self.assertEqual(first_project_name, times.first().project)

    def test_user_sort_date(self):
        # Check that view returns times for each user ordered by project name
        response = self.client.get('/users-view/?sort=date')
        times = WorkDay.objects.filter(user__username='chrxr').order_by('date')
        view_users = response.context['users']

        for user in view_users:
            for key, value in user.items():
                if key == "Chris Rogers":
                    first_date = value['times'][0].date

        self.assertEqual(response.status_code, 200)
        self.assertEqual(first_date, times.first().date)

    def test_unauthenticated_redirect(self):
        self.client.logout()
        response = self.client.get(reverse('users-view'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/users-view/")
