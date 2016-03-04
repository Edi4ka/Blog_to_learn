from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,  PermissionsMixin, AbstractUser


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey('blog.NewUser')
    tags = models.SlugField(blank=True, null=True)
    time_published = models.DateTimeField(auto_now_add=True)
    time_edited = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return '{0}'.format(self.title)

    def save(self, *args, **kwargs):
        if self.author.is_superuser:
            self.approved = True
        self.time_edited = timezone.now()
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey('blog.NewUser')
    text = models.TextField()
    time_published = models.DateTimeField(auto_now_add=True)
    time_edited = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return "Post's ID is {0}".format(self.comment.id)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        user = self.model(
            username=username,
            email=self.normalize_email(email), is_active=True)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.model(
            username=username,
            email=email,
            is_superuser=True,
            is_active=True,)
        user.set_password(password)
        user.save(using=self._db)
        return user


class NewUser(AbstractBaseUser,  PermissionsMixin):
    username = models.CharField(max_length=25, unique=True)
    password1 = models.CharField(max_length=25)
    password2 = models.CharField(max_length=25)
    date_birth = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=255)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_staff = models.IntegerField(default=False)
    is_active = models.BooleanField(default=False)

    object = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
