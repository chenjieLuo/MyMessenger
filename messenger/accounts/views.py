from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.generic import View
from .forms import UserForm, LoginForm, PostForm
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .models import Friend, Post


def home(request):
    return render(request, 'accounts/loggedin.html')


# def my_friends(request):
#    return render(request, 'accounts/my_friends.html')


# def my_messages(request):
#    return render(request, 'accounts/post.html', {'form': form, ''})


def show_user(request):
    query = request.GET.get("user_name")
    friend, created = Friend.objects.get_or_create(current_user=request.user)
    friends = friend.users.all()
    if query:
        users = User.objects.filter(
            Q(username__icontains=query)
        ).distinct()
        return render(request, 'accounts/show_user.html', {'users': users, 'friends': friends})

    return render(request, 'accounts/loggedin.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:home'))
        else:
            return redirect(reverse('accounts:change_password'))

    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'accounts/change_password.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('accounts/')


class My_Friends(TemplateView):
    template = 'accounts/friends.html'

    def get(self, request):
        users = User.objects.exclude(id=request.user.id)
        friend, created = Friend.objects.get_or_create(current_user=request.user)
        friends = friend.users.all()
        return render(request, self.template, {'users': users, 'friends': friends})


def change_friends(request, operation, id):
    friend = User.objects.get(id=id)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
    elif operation == 'remove':
        Friend.break_friend(request.user, friend)
    return render(request, 'accounts/loggedin.html')


class UserFormView(View):
    form_class_register = UserForm
    form_class_login = LoginForm
    template_name = 'accounts/register.html'
    login_template = 'accounts/loggedin.html'
    signup_template = 'accounts/signedup.html'

    def get(self, request):
        form = self.form_class_register(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class_register(None)
        form_register = self.form_class_register(request.POST)
        form_login = self.form_class_login(request.POST)

        if form_register.is_valid():
            user = form_register.save(commit=False)

            username = form_register.cleaned_data['username']
            password = form_register.cleaned_data['password']

            # password can be saved only using set function

            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            print("hello")
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, self.signup_template, {'form': form})
        if form_login.is_valid():
            username = form_login.cleaned_data['username']
            password = form_login.cleaned_data['password']

            user = authenticate(username=username, password=password)
            print("hello")
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, self.login_template, {'form': form})

        return render(request, self.template_name, {'form': form})


class PostView(TemplateView):
    form_post = PostForm
    template_name = 'accounts/post.html'

    def get(self, request):
        form = self.form_post(None)
        posts = Post.objects.all().order_by('-created')
        users = User.objects.exclude(id=request.user.id)

        return render(request, self.template_name, {'form': form, 'posts': posts, 'users': users})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            return redirect('accounts:my_messages')
        redirect('accounts:my_messages')
