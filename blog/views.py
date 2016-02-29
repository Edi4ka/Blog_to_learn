from django.shortcuts import render, redirect
from .models import Post, Comment
from django.utils import timezone
from .forms import AddComment, RegistrationForm
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
            comment = Comment(comment=post, author=author, text=form.text)
            comment.save()
            return redirect('blog.views.comments', post_id=post_id)
    else:
        form = AddComment()
    return render(request, 'blog/comment_page.html',
                  {'post': post, 'comment_list': comment_list,
                   'posts': posts, 'form': form, 'user': author})


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