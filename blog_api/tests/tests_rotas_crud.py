from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from blog.models import Post, Category
from django.contrib.auth.models import User


class PostTests(APITestCase):
    def setUp(self):
        self.url_list_create = reverse('blog_api:listcreate')
        self.url_detail = reverse(('blog_api:detailcreate'), kwargs={'pk': 1})
        self.test_category = Category.objects.create(name='django')
        self.test_category.save()

        self.test_user = User.objects.create_user(
            username='test_user1', 
            password='123456789')
        self.test_user.save()

        self.test_post = Post.objects.create(
            category_id= self.test_category.id, 
            title='Post Title', 
            excerpt='Post Excerpt', 
            content='Post Content', 
            slug='post-title', 
            author_id= self.test_user.id, 
            status='published')
        self.test_post.save()
        
        self.data = {
            "title": "new", 
            "author": 1,
            "excerpt": "new", 
            "content": "new"
        }

    def test_view_get_all(self):
        """ Verifica a consulta dos objetos """
        response = self.client.get(self.url_list_create, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_post(self):
        """ Verifica se o post foi criado com sucesso """
        response = self.client.post(self.url_list_create, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 6)

    def test_view_get_id(self):
        """ Verifica se ta retornando o post pelo id """
        response = self.client.get(self.url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_delete(self):
        """ Verifica se esta deletando pelo id """
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
