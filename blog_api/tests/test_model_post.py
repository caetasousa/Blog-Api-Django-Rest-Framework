from django.test import TestCase
from datetime import datetime
from blog_api.models import Post, Category
from django.contrib.auth import get_user_model


class TestCreatePost(TestCase):
    def setUp(self):
        db = get_user_model()
        self.test_category = Category.objects.create(name='django')

        self.test_user = db.objects.create_user(
                            'testuser@user.com', 
                            'test_user', 
                            'firstname', 
                            '123456789')

        self.test_post = Post.objects.create(
            category_id= self.test_category.id, 
            title='Post Title', 
            excerpt='Post Excerpt', 
            content='Post Content', 
            slug='post-title', 
            author_id= self.test_user.id, 
            status='published')

        self.post = Post.postobjects.get(id=1)
        
    def test_create(self):
        ''' Checa se o usuario existe no banco '''
        self.assertTrue(Post.objects.exists())

    def test_post_category_field(self):
        ''' Verifica a relação com categoria '''
        category = f'{self.post.category}'
        self.assertEqual(category, 'django')
    
    def test_post_author_field(self):
        ''' Verifica a relação com author '''
        author = f'{self.post.author}'
        self.assertEqual(author, 'test_user')

    def test_create_at(self):
        '''Verifica hora da publicação'''
        self.assertIsInstance(self.post.published, datetime)

    def test_email_can_be_blank(self):
        ''' Verifica se o field pode ser nulo '''
        field = Post._meta.get_field('excerpt')
        self.assertTrue(field.null)

    def test_post_title_field(self):
        ''' Verifica o title '''
        title = f'{self.post.title}'
        self.assertEqual(title, 'Post Title')

    def test_post_excerpt_field(self):
        ''' Verifica o excerpt '''
        excerpt = f'{self.post.excerpt}'
        self.assertEqual(excerpt, 'Post Excerpt')

    def test_post_content_field(self):
        ''' Verifica o content '''
        content = f'{self.post.content}'
        self.assertEqual(content, 'Post Content')
    
    def test_post_slug_field(self):
        ''' Verifica o slug '''
        slug = f'{self.post.slug}'
        self.assertEqual(slug, 'post-title')

    def test_post_status_field(self):
        ''' Verifica o status '''
        status = f'{self.post.status}'
        self.assertEqual(status, 'published')

    

