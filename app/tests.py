from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth import views
from django.contrib.auth import get_user_model
from .models import WorkDay, Project
from .forms import WorkDayForm, CreateAccountForm

class TimeTestUtils(object):

    @staticmethod
    def create_test_user():
        """
        Override this method to return an instance of your custom user model
        """
        user_model = get_user_model()
        # Create a user
        user_data = dict()
        user_data[user_model.USERNAME_FIELD] = 'test@email.com'
        user_data['password'] = 'password'

        for field in user_model.REQUIRED_FIELDS:
            user_data[field] = field

        return user_model.objects.create_superuser(**user_data)

    def login(self):
        user = self.create_test_user()

        user_model = get_user_model()
        # Login
        self.assertTrue(
            self.client.login(password='password', **{user_model.USERNAME_FIELD: 'test@email.com'})
        )

        return user


class TestWorkDay(TestCase):

    def setUp(self):
        Project.objects.create(projectName="Awesome Project")
        get_user_model().objects.create_superuser(username='test', email='test@email.com', password='password')
        project = Project.objects.get(projectName="Awesome Project")
        user = User.objects.get(username="test")
        WorkDay.objects.create(date="2016-02-02", project=project, hours="7.5", days="1", user=user)

    def test_work_day_object(self):
        time = WorkDay.objects.get(pk=1)

        self.assertEqual(time.hours, 7.5)
        self.assertEqual(time.project.projectName, "Awesome Project")
        self.assertEqual(time.days, "1")
        self.assertEqual(time.user.username, "test")


class TestWorkDayForm(TestCase, TimeTestUtils):

    def setUp(self):
        Project.objects.create(projectName="Awesome Project")
        get_user_model().objects.create_superuser(username='test', email='test@email.com', password='password')

    def test_valid_data(self):
        user = get_user_model().objects.get(username='test')

        project = Project.objects.get(projectName="Awesome Project")
        form = WorkDayForm({'days':'1','project': project.id,'date': '2016-02-02'})
        self.assertTrue(form.is_valid())
        new_time = form.save(commit=False)

        self.assertEqual(new_time.days, "1")
        self.assertEqual(new_time.project.projectName, "Awesome Project")

        new_time.user = user
        new_time.save()

        times = WorkDay.objects.all()

        self.assertTrue(len(times) > 0)

    def test_invalid_data(self):
        self.login()
        project = Project.objects.get(projectName="Awesome Project")
        # form = WorkDayForm({'days':'1','project': project.id,'date': '02-02-02'})
        response = self.client.post('/logtime/',{
            'days':'1',
            'project': project.id,
            'date': '02-02-02'
        })
        self.assertTemplateUsed('app/workdayform.html')
        self.assertContains(response, "Enter a valid date.")

    def test_valid_form_redirect(self):
        self.login()
        project = Project.objects.get(projectName="Awesome Project")
        response = self.client.post('/logtime/',{
            'days':'1',
            'project': project.id,
            'date': '2016-02-02'
        })

        self.assertRedirects(response, reverse('view-my-times'))


class TestAuthentication(TestCase, TimeTestUtils):

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_view_post(self):
        get_user_model().objects.create_superuser(username='test', email='test@email.com', password='password')

        response = self.client.post(reverse('login'), {
            'username': 'test',
            'password': 'password',
        })

        # self.assertRedirects(response, reverse('log-time'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/logtime', target_status_code=301)

        self.assertTrue('_auth_user_id' in self.client.session)
        self.assertEqual(
            str(self.client.session['_auth_user_id']),
            str(get_user_model().objects.get(username='test').id)
        )

    def test_managers_header(self):
        Group.objects.create(name='manager')
        managers_group = Group.objects.get(name='manager')
        get_user_model().objects.create_superuser(username='test', email='test@email.com', password='password')
        user = get_user_model().objects.get(username='test')
        managers_group.user_set.add(user)

        self.assertTrue(self.client.login(username='test', password='password'))
        response = self.client.get(reverse('log-time'))

        self.assertContains(response, 'PROJECTS VIEW')

    def test_regular_header(self):
        self.login()
        response = self.client.get(reverse('log-time'))

        self.assertNotContains(response, 'PROJECTS VIEW')


class TestAccountCreation(TestCase):

    def test_account_creation_form(self):
        form = CreateAccountForm({
            "username": 'test',
            "email": "test@test.com",
            "password1": "secret",
            "password2": "secret",
        })
        self.assertTrue(form.is_valid())
        form.save()
        user = get_user_model().objects.get(username='test')
        self.assertEqual(user.username, 'test')

    def test_clean_password2(self):
        form = CreateAccountForm({
            "username": 'test',
            "email": "test@test.com",
            "password1": "secret",
            "password2": "secret2",
        })

        response = self.client.post(reverse("create-account"), {
            "username": 'test',
            "email": "test@test.com",
            "password1": "secret",
            "password2": "secret2",
        })
        self.assertContains(response, "The two password fields didn&#39;t match.")

        user = get_user_model().objects.filter(username='test')
        self.assertFalse(user)
