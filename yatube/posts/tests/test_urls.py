from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Group, Post, User

from http import HTTPStatus


class StaticURLTests(TestCase):
    def test_static_pages_status(self):
        templates_url_names = {
            '/about/author/': '',
            '/about/tech/': '',
        }
        for address in templates_url_names:
            response = self.client.get(address)
            self.assertEqual(response.status_code, HTTPStatus.OK)


class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.group = Group.objects.create(
            title='Текст поста',
            slug='test_slug',
            description='Описание поста'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст поста',
            group=cls.group
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': f'/group/{PostURLTest.group.slug}/',
            'posts/profile.html': f'/profile/{PostURLTest.user}/',
            'posts/post_detail.html': f'/posts/{PostURLTest.post.id}/',
            'posts/create_post.html': '/create/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_redirect_if_not_auth(self):
        response = self.client.get('/create/', follow=True)
        path = reverse('users:login')
        self.assertRedirects(
            response, f'{path}?next=/create/',
        )

    def test_404_page(self):
        response = self.client.get('/wrong_url/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
