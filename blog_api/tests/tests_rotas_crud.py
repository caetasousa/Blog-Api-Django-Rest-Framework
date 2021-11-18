from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from blog_api.models import Post, Category
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


class PostTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.db = get_user_model()

        self.url_list_create = reverse('blog_api:listcreate')
        self.url_detail = reverse(('blog_api:detailcreate'), kwargs={'pk': 1})
        
        #Criando categoria no banco
        self.test_category = Category.objects.create(name='django')

        #Usuario 1
        self.super_user = self.db.objects.create_superuser(
                            'testuser@user.com', 
                            'test_user', 
                            'firstname', 
                            '123456789')

        #Usuario 2
        self.test_user2 = self.db.objects.create_user(
                            'testuser2@user.com', 
                            'test_user2', 
                            'test_user2', 
                            '123456789')

        #Usuario 3
        self.test_user3 = self.db.objects.create_user(
                            'testuser3@user.com', 
                            'test_user3', 
                            'test_user3', 
                            '123456789')

        #Criando Post no banco
        self.test_post = Post.objects.create(
            category_id= self.test_category.id, 
            title='Post Title', 
            excerpt='Post Excerpt', 
            content='Post Content', 
            slug='post-title', 
            author_id= self.test_user2.id, 
            status='published')
        
        #Objeto para criar post pela url
        self.data = {
            "title": "New",
            "author": 1,
            "excerpt": "New",
            "content": "New",
            "status": "published"
        }
        #Objeto para criar o update
        self.update = {
            "title": "New",
            "author": 3,
            "excerpt": "New",
            "content": "casa",
            "status": "published"
        }

    def test_view_get_all(self):
        """ Verifica a consulta dos objetos """
        response = self.client.get(self.url_list_create, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_get_id(self):
        """ Verifica se ta retornando o post pelo id """
        response = self.client.get(self.url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_post(self):
        """ Verifica se o post foi criado com sucesso, qualquer usuario pode criar um post """
        user = self.db.objects.get(user_name=self.test_user2.user_name)
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url_list_create, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 7)    

    def test_view_delete_superuser(self):
        """ Verifica a exclusão com usuario superuser """
        user = self.db.objects.get(user_name=self.super_user.user_name)
        self.client.force_authenticate(user=user)
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_view_delete_author_is_the_user_creator(self):
        """ Verifica se quem ta excluindo e quem criou o post"""
        user = self.db.objects.get(user_name=self.test_user2.user_name)
        self.client.force_authenticate(user=user)
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_view_delete_author_not_a_creator_and_not_superuser(self):
        """ Não deixa um usuario diferente de superuser ou criador do post excluir """
        user = self.db.objects.get(user_name=self.test_user3.user_name)
        self.client.force_authenticate(user=user)
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_update_user_superuser(self):
        """ Faz o update pelo superuser """
        user = self.db.objects.get(user_name=self.super_user.user_name)
        self.client.force_authenticate(user=user)
        response = self.client.put(self.url_detail, self.update, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_update_author_is_the_user_creator(self):
        """ Faz o update pelo criador do post"""
        user = self.db.objects.get(user_name=self.test_user2.user_name)
        self.client.force_authenticate(user=user)
        response = self.client.put(self.url_detail, self.update, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_update_author_not_a_creator_and_not_superuser(self):
        """ Não deixa com que outro que n seja o super user ou o criador do post fazer mudancas """
        user = self.db.objects.get(user_name=self.test_user3.user_name)
        self.client.force_authenticate(user=user)
        response = self.client.put(self.url_detail, self.update, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)