from django.test import TestCase
from django.contrib.auth.models import User

class TestCreateUser(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='test_user', 
            password='123456789')

        self.test_user.save()

        # para checar o password
        self.user = User.objects.get(username="test_user")

    def test_create(self):
        ''' Checa se o usuario existe no banco '''
        self.assertTrue(User.objects.exists())

    def test_username_field(self):
        ''' Verifica o username '''
        username = self.test_user.username
        self.assertEqual(username, 'test_user')

    def test_password_field(self):
        ''' Verifica o password '''
        self.assertEqual(self.user.check_password("123456789"), True)

    def test_email_can_be_blank(self):
        ''' Verifica se o field pode ser em branco '''
        field = User._meta.get_field('email')
        self.assertTrue(field.blank)

    def test_str(self):
        ''' Verifica o __str__ do model'''
        self.assertEqual('test_user', str(self.test_user))