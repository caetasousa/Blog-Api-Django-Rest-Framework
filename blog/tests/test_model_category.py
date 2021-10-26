from django.test import TestCase
from blog.models import Category


class TestCreateCategory(TestCase):
    def setUp(self):
        self.test_category = Category.objects.create(name='django')

    def test_create(self):
        ''' Checa se o usuario existe no banco '''
        self.assertTrue(Category.objects.exists())

    def test_name_field(self):
        ''' Verifica o name '''
        name = self.test_category.name
        self.assertEqual(name, 'django')
    
    def test_str(self):
        ''' Verifica o __str__ do model'''
        self.assertEqual('django', str(self.test_category))

    



