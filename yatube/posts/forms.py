from django.forms import ModelForm

from .models import Post, Comment, Follow


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group', 'image']
        labels = {
            'text': 'Текст',
            'group': 'Группа',
            'image': 'Картинка',
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'Текст',
        }


class FollowForm(ModelForm):
    class Meta:
        model = Follow
        fields = ('author',)
        labels = {
            'author': 'Пользователь',
        }
