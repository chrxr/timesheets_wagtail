from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group

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
