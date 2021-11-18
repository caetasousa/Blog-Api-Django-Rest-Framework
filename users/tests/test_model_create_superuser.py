from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import NewUser


class TestCreateSuperUser(TestCase):
    def setUp(self):
        self.db = get_user_model()
        self.super_user = self.db.objects.create_superuser(
                            'testuser@user.com', 
                            'test_user', 
                            'firstname', 
                            '123456789')

        # para checar o password
        self.user = self.db.objects.get(user_name="test_user")

    def test_create(self):
        ''' Checa se o usuario existe no banco '''
        self.assertTrue(self.db.objects.exists())

    def test_firstname_field(self):
        ''' Verifica o username '''
        first_name = self.super_user.first_name
        self.assertEqual(first_name, 'firstname')
    
    def test_email_field(self):
        ''' Verifica o username '''
        email = self.super_user.email
        self.assertEqual(email, 'testuser@user.com')

    def test_username_field(self):
        ''' Verifica o username '''
        username = self.super_user.user_name
        self.assertEqual(username, 'test_user')

    def test_password_field(self):
        ''' Verifica o password '''
        self.assertEqual(self.user.check_password("123456789"), True)

    def test_email_can_be_blank(self):
        ''' Verifica se o field pode ser em branco '''
        field = NewUser._meta.get_field('about')
        self.assertTrue(field.blank)

    def test_is_active_field(self):
        ''' Verifica o username '''
        is_active = self.super_user.is_active
        self.assertEqual(is_active, True)

    def test_superuser_field(self):
        ''' Verifica o username '''
        is_superuser = self.super_user.is_superuser
        self.assertEqual(is_superuser, True)

    def test_is_staff_field(self):
        ''' Verifica o username '''
        is_staff = self.super_user.is_staff
        self.assertEqual(is_staff, True)

    def test_str(self):
        ''' Verifica o __str__ do model'''
        self.assertEqual('test_user', str(self.super_user.user_name))
