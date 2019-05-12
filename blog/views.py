from django.shortcuts import render
from .models import Post, Topic
from .forms import LoginForm, RegistrationForm, TopicForm, PostForm
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import Group, User
from django.http import Http404


def post_list(request):
    posts = Post.objects.all()
    is_moder = check_user(request.user)
    return render(request, 'blog/post_list.html', {'posts': posts, 'is_moderator': is_moder,
                                                   'left_menu': left_menu()})


def add_post(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'blog/post_form.html', {'is_moderator': check_user(request.user),
                                                       'left_menu': left_menu(), 'form': form})
    else:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            if new_post.published and check_user(request.user):
                new_post.publish()
                form.save_m2m()
            else:
                new_post.save()
                form.save_m2m()
            return redirect('post_list')
        else:
            return render(request, 'blog/post_form.html', {'is_moderator': check_user(request.user),
                                                           'left_menu': left_menu(), 'form': form})


def delete_post(request, pk):
    if check_user(request.user):
        for p in Post.objects.filter(pk=pk):
            p.delete()
        return redirect('post_list')
    else:
        raise Http404


def edit_post(request, pk):
    current_post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        form = PostForm(instance=current_post)
        return render(request, 'blog/post_form.html', {'is_moderator': check_user(request.user),
                                                       'left_menu': left_menu(), 'form': form, 'pk': pk})
    else:
        form = PostForm(request.POST, request.FILES, instance=current_post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            if new_post.published and check_user(request.user):
                new_post.publish()
                form.save_m2m()
            else:
                new_post.save()
                form.save_m2m()
            return redirect('post_list')
        else:
            return render(request, 'blog/post_form.html', {'is_moderator': check_user(request.user),
                                                           'left_menu': left_menu(), 'form': form, 'pk': pk})


def read_post(request, pk):
    current_post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/read_post.html', {'post': current_post, 'is_moderator': check_user(request.user),
                                                   'left_menu': left_menu()})


def topics_list(request):
    topics = Topic.objects.all()
    is_moder = check_user(request.user)
    if is_moder:
        form = TopicForm()
    else:
        form = None
    return render(request, 'blog/topics_list.html', {'topics': topics, 'is_moderator': is_moder,
                                                     'left_menu': left_menu(), 'form': form})


def add_topic(request):
    if request.method == 'POST':
        topic = TopicForm(request.POST, request.FILES)
        if topic.is_valid():
            topic.save()
            return redirect('topics_list')
        else:
            topics = Topic.objects.all()
            is_moder = check_user(request.user)
            return render(request, 'blog/topics_list.html', {'topics': topics, 'is_moderator': is_moder,
                                                             'left_menu': left_menu(), 'form': topic})
    else:
        return redirect('topics_list')


def topic_edit(request, pk):
    current_topic = get_object_or_404(Topic, pk=pk)
    posts_count = current_topic.post_set.all().count()
    topics = Topic.objects.all().exclude(pk=pk)
    is_moder = check_user(request.user)
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES, instance=current_topic)
        if form.is_valid():
            form.save()
            return redirect('topics_list')
    else:
        if is_moder:
            form = TopicForm(instance=current_topic)
        else:
            form = None
    return render(request, 'blog/topics_list.html', {'topics': topics, 'is_moderator': is_moder,
                                                     'left_menu': left_menu(), 'form': form,
                                                     'total_posts': 'Всего постов в этой теме: ' + posts_count.__str__(),
                                                     'pk': pk})


def topic_delete(request, pk):
    current_topic = get_object_or_404(Topic, pk=pk)
    current_topic.delete()
    return redirect('topics_list')


"""Получение из данных для левого меню из БД"""


def left_menu():
    left_menu = {
        'top_topics': Topic.objects.all(),  # попробовать написать свой менеджер, для вывода ТОП-10(Topic.TOP_TEN.all())
        'top_authors': User.objects.all()
    }
    return left_menu


"""Проверка, что юзер - модератор"""


def check_user(usr):
    is_moder = False

    if usr.is_authenticated:
        grp = Group.objects.get(name='Модераторы')
        if grp in usr.groups.all():
            is_moder = True
    return is_moder


def logout_user(request):
    logout(request)
    posts = Post.objects.all()
    return redirect('post_list')


def login_page(request):
    if not request.user.is_authenticated:
        form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})
    return redirect('post_list')


def registration_page(request):
    if not request.user.is_authenticated:
        form = RegistrationForm()
        return render(request, 'blog/registration.html', {'form': form})
    return redirect('post_list')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        error = None
        if form.is_valid():
            sucss = 'Регистрация прошла успешно. Теперь вы можете авторизоваться на сайте!'
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            readers = Group.objects.get(name='Читатели')
            readers.user_set.add(new_user)
            form = LoginForm(request.POST)
            return render(request, 'blog/login.html', {'form': form, 'success': sucss})
        else:
            return render(request, 'blog/registration.html', {'form': form, 'error': error})


def login_user(request):
    if request.method == 'POST':
        usr_form = LoginForm(request.POST)
        print(usr_form.is_valid())
        print(usr_form.errors)
        if usr_form.is_valid():
            user = authenticate(request, username=usr_form.cleaned_data['username'],
                                password=usr_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('post_list')
            else:
                usr_form.add_error('username', 'Не верный логин или пароль')
                return render(request, 'blog/login.html', {'form': usr_form})
        else:
            return render(request, 'blog/login.html', {'form': usr_form})
    else:
        form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})

# Create your views here.
