from users.models  import NewUser
from django.test import TestCase
from blog_api.models import Post, Category
from blog_api.serializers import PostSerializer
from django.contrib.auth import get_user_model


class PostSerializerTestCase(TestCase):
    def setUp(self):
        self.db = get_user_model()
        self.test_user = self.db.objects.create_user(
                            'testuser@user.com', 
                            'test_user', 
                            'firstname', 
                            '123456789')

        self.test_category = Category.objects.create(name='django')

        self.test_post = Post.objects.create(
            category_id= self.test_category.id, 
            title='Post Title', 
            excerpt='Post Excerpt', 
            content='Post Content', 
            slug='post-title', 
            author_id= self.test_user.id, 
            status='published')

        self.serializer = PostSerializer(instance=self.test_post)
        self.data = self.serializer.data

    def test_fields_post_serializer(self):
        """ Teste que verifica os campos que estão sendo serializados """
        self.assertEqual(set(self.data.keys()), set(['id', 'title', 'author', 'excerpt', 'content', 'status', 'category'] ))

    def test_content_serializer_title(self):
        """ Verifica o conteudo de title """
        self.assertEqual(self.data['title'], self.test_post.title)

    def test_content_serializer_excerpt(self):
        """ Verifica o conteudo de excerpt """
        self.assertEqual(self.data['excerpt'], self.test_post.excerpt)

    def test_content_serializer_content(self):
        """ Verifica o conteudo de content """
        self.assertEqual(self.data['content'], self.test_post.content)

    def test_content_serializer_author(self):
        """ Verifica o conteudo de author """
        self.assertEqual(self.data['author'], self.test_post.author_id)
    
    def test_content_serializer_category(self):
        """ Verifica o conteudo de author """
        self.assertEqual(self.data['category'], self.test_post.category_id)

    def test_content_serializer_status(self):
        """ Verifica o conteudo de status """
        self.assertEqual(self.data['status'], self.test_post.status)
    
