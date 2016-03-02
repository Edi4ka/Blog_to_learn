from django.shortcuts import render, redirect
from .models import Post, Comment
from django.utils import timezone
from .forms import AddComment, RegistrationForm, LoginUser, AddPost, EditComment
from django.contrib.auth import authenticate, login


def main_page(request):
    posts = Post.objects.all()
    return render(request, 'blog/main_page.html', {'posts': posts})


def comments(request, post_id):
    author = request.user
    posts = Post.objects.all()
    post = Post.objects.get(pk=post_id)
    comment_list = post.comment_set.all()
    if request.method == 'POST':
        form = AddComment(request.POST)
        if form.is_valid():
            comment = Comment(comment=post,
                              author=author,
                              text=form.text)
            comment.save()
            return redirect('blog.views.comments', post_id=post_id)
    else:
        form = AddComment()
    return render(request, 'blog/comment_page.html',
                  {'post': post, 'comment_list': comment_list,
                   'posts': posts, 'form': form, 'author': author})


def add_post(request):
    author = request.user
    if request.method == 'POST':
        form = AddPost(request.POST)
        if form.is_valid():
            post = Post(text=form.text_,
                        title=form.title_,
                        author=author,
                        tags=form.tags_)
            post.save()
            return redirect('blog.views.comments', post_id=post.id)
    else:
        form = AddPost()
    return render(request, 'blog/add_post.html', {"form": form})


def edit_comment(request, comment_id):
    user = request.user
    if user == Comment.objects.get(id=comment_id).author:
        if request.method == 'POST':
            form = EditComment(request.POST)
            if form.is_valid():
                pass
            ##Доделать сохранение комментария
        else:
            form = EditComment(Comment.objects.get(id=comment_id))
    else:
        return redirect('blog.views.main_page')
    return render(request, 'blog/edit_comment.html', {'form': form})


def registration_form(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=request.POST.get('username'),
                                password=request.POST.get('password1'))
            login(request, user)
            return render(request, 'blog/registration_successful.html')
    else:
        form = RegistrationForm()
    return render(request, 'blog/registration.html', {"form": form})


def registration_success(request):
    return render(request, 'blog/registration_successful.html')


def login_user(request):
    if request.method == "POST":
        form = LoginUser(data=request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST.get('username'),
                                password=request.POST.get('password'))
            if user is not None:
                login(request, user)
                return redirect('blog.views.main_page')
    else:
        form = LoginUser()
    return render(request, 'blog/login.html', {'form': form})