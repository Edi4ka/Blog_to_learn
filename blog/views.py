from django.shortcuts import render, redirect
from .models import Post, Comment, RatingPost, RatingComment
from .forms import AddComment, AddPost, EditComment, RegistrationForm, LoginUser, EditPost
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404


def main_page(request):
    author = request.user
    posts = Post.objects.filter(time_published__lte=timezone.now()).order_by('time_published').reverse()
    paginated = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        post_list = paginated.page(page)
    except PageNotAnInteger:
        post_list = paginated.page(1)
    except EmptyPage:
        post_list = paginated.page(paginated.num_pages)

    return render(request, 'blog/main_page.html', {'post_list': post_list, 'author' : author})


def comments(request, post_id):
    author = request.user
    posts = Post.objects.all()
    post = Post.objects.get(pk=post_id)
    comment_list = post.comment_set.all()
    if request.method == 'POST':
        form = AddComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comment = post
            comment.author = author
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
            post = form.save(commit=False)
            post.author = author
            post.save()
            post_id = post.id
            return redirect('blog.views.comments', post_id=post_id)
    else:
        form = AddPost()

    return render(request, 'blog/add_post.html', {'form': form})


def edit_comment(request, comment_id):
    user = request.user

    if user == Comment.objects.get(id=comment_id).author:
        if request.method == 'POST':
            form = EditComment(request.POST)
            if form.is_valid():
                comment = Comment.objects.get(pk=comment_id)
                comment.text = form.text_to_view
                comment.time_edited = timezone.now()
                comment.save()
                return redirect('blog.views.comments', post_id=comment.comment.id)
        else:
            form = EditComment(initial=
                               {'text': Comment.objects.get(id=comment_id).text})
    else:
        return redirect('blog.views.main_page')

    return render(request, 'blog/edit_comment.html', {'form': form})


def edit_post(request, post_id):
    user = request.user

    if user == Post.objects.get(id=post_id).author:
        if request.method == 'POST':
            form = EditPost(request.POST)
            if form.is_valid():
                post = Post.objects.get(pk=post_id)
                post.text = form.text_to_view
                post.title = form.title_to_view
                post.time_edited = timezone.now()
                post.save()
                return redirect('blog.views.comments', post_id=post_id)
        else:
            form = EditPost(initial=
                            {'text': Post.objects.get(id=post_id).text,
                             'title': Post.objects.get(id=post_id).title})
    else:
        return redirect('blog.views.main_page')
    return render(request, 'blog/edit_post.html', {"form": form})


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('blog.views.comments', post_id=comment.comment.id)


def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('blog.views.main_page')


def approve_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)
    post.approved = True
    post.save()
    return redirect('blog.views.personal', username=user)


def add_plus_post(request, post_id):
    user = request.user
    post = Post.objects.get(pk=post_id)
    if len(RatingPost.objects.filter(post=post, rating_author=user)) == 0:
        post.rating += 1
        post.save()
        plus_added = RatingPost(post=Post.objects.get(pk=post_id), rating_author=user)
        plus_added.save()
        return redirect('blog.views.comments', post_id=post_id)
    return redirect('blog.views.comments', post_id=post_id)


def add_minus_post(request, post_id):
    user = request.user
    post = Post.objects.get(pk=post_id)
    if len(RatingPost.objects.filter(post=post, rating_author=user)) == 0:
        post.rating -= 1
        post.save()
        RatingPost(post=Post.objects.get(pk=post_id), rating_author=user).save()
        return redirect('blog.views.comments', post_id=post_id)
    return redirect('blog.views.comments', post_id=post_id)


def add_plus_comment(request, comment_id):
    user = request.user
    comment = Comment.objects.get(pk=comment_id)
    if len(RatingComment.objects.filter(comment=comment, rating_author=user)) == 0:
        comment.rating += 1
        comment.save()
        plus_added = RatingComment(comment=Comment.objects.get(pk=comment_id), rating_author=user)
        plus_added.save()
        return redirect('blog.views.comments', post_id=comment.comment.id)
    return redirect('blog.views.comments', post_id=comment.comment.id)


def add_minus_comment(request, comment_id):
    user = request.user
    comment = Comment.objects.get(pk=comment_id)
    if len(RatingComment.objects.filter(comment=comment, rating_author=user)) == 0:
        comment.rating -= 1
        comment.save()
        plus_added = RatingComment(comment=Comment.objects.get(pk=comment_id), rating_author=user)
        plus_added.save()
        return redirect('blog.views.comments', post_id=comment.comment.id)
    return redirect('blog.views.comments', post_id=comment.comment.id)


def registration_form(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            user = authenticate(username=request.POST.get('username'),
                                password=request.POST.get('password2'))
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


def personal(request, username):
    posts_to_approve = Post.objects.filter(approved=False)
    user = request.user
    user_rating = sum([x.rating for x in Post.objects.filter(author=user)] +
                      [x.rating for x in Comment.objects.filter(author=user)])
    user_comments = Comment.objects.filter(author=user).count()
    user_posts = Post.objects.filter(author=user).count()
    return render(request, 'blog/personal.html', {'username': username,
                                                  'user_rating': user_rating,
                                                  'user_comments': user_comments,
                                                  'user_posts': user_posts,
                                                  'posts_to_approve': posts_to_approve,
                                                  'user': user})


def tag_list(request):
    tags_list = Post.objects.all()
    return render(request, 'blog/tag_list.html', {'tag_list': tags_list})


def main_info(request):
    return render(request, 'blog/main_info.html')
