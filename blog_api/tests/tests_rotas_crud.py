from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from blog_api.models import Post, Category
from django.contrib.auth.models import User
from rest_framework.test import APIClient


class PostTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.url_list_create = reverse('blog_api:listcreate')
        self.url_detail = reverse(('blog_api:detailcreate'), kwargs={'pk': 1})
        
        #Criando categoria no banco
        self.test_category = Category.objects.create(name='django')
        self.test_category.save()

        #Usuario 1
        self.test_user1 = User.objects.create_superuser(
            username='test_user1', 
            password='123456789')
        self.test_user1.save()

        #Usuario 2
        self.test_user2 = User.objects.create_user(
            username='test_user2', password='123456789')
        self.test_user2.save()

        #Usuario 3
        self.test_user3 = User.objects.create_user(
            username='test_user3', password='123456789')
        self.test_user2.save()

        #Criando Post no banco
        self.test_post = Post.objects.create(
            category_id= self.test_category.id, 
            title='Post Title', 
            excerpt='Post Excerpt', 
            content='Post Content', 
            slug='post-title', 
            author_id= self.test_user2.id, 
            status='published')
        self.test_post.save()
        
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
        self.client.login(username=self.test_user2.username, password='123456789')#logando usuario
        response = self.client.post(self.url_list_create, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 7)    

    def test_view_delete_superuser(self):
        """ Verifica a exclusão com usuario superuser """
        self.client.login(username=self.test_user1.username, password='123456789')#logando usuario1
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_view_delete_author_is_the_user_creator(self):
        """ Verifica se quem ta excluindo e quem criou o post"""
        self.client.login(username=self.test_user2.username, password='123456789')#logando usuario2
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_view_delete_author_not_a_creator_and_not_superuser(self):
        """ Não deixa um usuario diferente de superuser ou criador do post excluir """
        self.client.login(username=self.test_user3.username, password='123456789')#logando usuario3
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_update_user_superuser(self):
        """ Faz o update pelo superuser """
        self.client.login(username=self.test_user1.username, password='123456789')#logando usuario1
        response = self.client.put(self.url_detail, self.update, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_update_author_is_the_user_creator(self):
        """ Faz o update pelo criador do post"""
        self.client.login(username=self.test_user2.username, password='123456789')#logando usuario2
        response = self.client.put(self.url_detail, self.update, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_update_author_not_a_creator_and_not_superuser(self):
        """ Não deixa com que outro que n seja o super user ou o criador do post fazer mudancas """
        self.client.login(username=self.test_user3.username, password='123456789')#logando usuario3
        response = self.client.put(self.url_detail, self.update, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)