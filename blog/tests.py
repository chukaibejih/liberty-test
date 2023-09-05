from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Blog, BlogSharing
from .serializers import BlogSerializer, BlogSharingSerializer

User = get_user_model()

class BlogViewsetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_create_blog(self):
        url = reverse('blog-list')
        data = {
            'title': 'Test Blog',
            'content': 'This is a test blog content.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blog.objects.count(), 1)
        self.assertEqual(Blog.objects.get().title, 'Test Blog')
    
    def test_update_blog(self):
        blog = Blog.objects.create(
            title='Original Title',
            content='Original Content',
            author=self.user
        )
        url = reverse('blog-detail', kwargs={'pk': blog.id})
        updated_data = {
            'title': 'Updated Title',
            'content': 'Updated Content'
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        blog.refresh_from_db()
        self.assertEqual(blog.title, 'Updated Title')


class BlogSharingViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_share_blog(self):
        blog = Blog.objects.create(
            title='Test Blog',
            content='This is a test blog content.',
            author=self.user
        )
        url = reverse('share-blog')
        data = {
            'shared_with': self.user.id,
            'blog': blog.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogSharing.objects.count(), 1)
    

class AuthorsWithAccessViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_authors_with_access(self):
        blog = Blog.objects.create(
            title='Test Blog',
            content='This is a test blog content.',
            author=self.user
        )
        sharing = BlogSharing.objects.create(
            owner=self.user,
            shared_with=self.user,
            blog=blog
        )
        url = reverse('authors-with-access')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
