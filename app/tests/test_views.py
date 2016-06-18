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
        project = Project.objects.get(projectName="Talbot")
        self.assertEqual(project.projectName, "Talbot")
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
        times = WorkDay.objects.filter(project__projectName='Talbot').order_by('user__first_name')
        view_projects = response.context['projects']
        first_user = view_projects['Talbot']['times'][0].user

        self.assertEqual(response.status_code, 200)
        self.assertEqual(first_user, times.first().user)

    def test_project_sort_date(self):
        # Check that view returns times for each project ordered by date
        response = self.client.get('/projects-view/?sort=date')
        times = WorkDay.objects.filter(project__projectName='Talbot').order_by('date')
        view_projects = response.context['projects']
        first_date = view_projects['Talbot']['times'][0].date

        self.assertEqual(response.status_code, 200)
        self.assertEqual(first_date, times.first().date)
