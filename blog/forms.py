from django.contrib.auth.models import User
from django import forms
from blog.models import Topic, Post


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True)

    # class Meta:
    # 	model = User
    # 	fields = ('username', 'password')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')

        if username:
            if User.objects.filter(username=username).first() is None:
                self.add_error('username', 'Не верный логин или пароль')


class RegistrationForm(forms.ModelForm):
    password_confirmation = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')

    def clean(self):
        cleaned_data = super().clean()
        password_confirmation = cleaned_data.get("password_confirmation")
        password = cleaned_data.get("password")
        email = cleaned_data.get("email")

        if password_confirmation and password:
            if password_confirmation != password:
                self.add_error('password', 'Пароли не совпадают!')
        else:
            self.add_error('password', 'Введите пароль и подтверждение!')

        if email:
            if User.objects.filter(email=email).first() is not None and email.strip() != '':
                self.add_error('email', 'E-mail занят!')


class TopicForm(forms.ModelForm):
    class Meta(object):
        model = Topic
        fields = ('title', 'image')


class PostForm(forms.ModelForm):
    class Meta(object):
        model = Post
        fields = ('title', 'text', 'topics', 'image', 'published')
