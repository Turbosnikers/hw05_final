from django.test import TestCase

from ..models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth_user')
        cls.group = Group.objects.create(
            title='заголовок поста',
            slug='test_slug',
            description='Описание поста',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст поста',
            group=cls.group
        )

    def test_post_text_str(self):
        post = PostModelTest.post
        self.assertEqual(post.text[:15], str(post))

    def test_group_title_str(self):
        title = PostModelTest.group.title
        self.assertEqual(title, str(title))
