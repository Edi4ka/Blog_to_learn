from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey('auth.User')
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
    author = models.ForeignKey('auth.User')
    text = models.TextField()
    time_published = models.DateTimeField(auto_now_add=True)
    time_edited = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return "Post's ID is {0}".format(self.comment.id)


class User(AbstractBaseUser):
    username = models.CharField(max_length=25, unique=True)
    password1 = models.CharField(max_length=25)
    password2 = models.CharField(max_length=25)
    date_birth = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=255)
    registration_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['username', 'password1', 'password2', 'date_birth', 'email']
    USERNAME_FIELD = 'username'


class UserManager(BaseUserManager):
    def create_user(self, email, password, registration_date, **kwargs):
        user = self.model(email=self.normalize_email(email),
                          registration_date=timezone.now(),
                          is_active=True,
                          **kwargs)
        user.set_password(password)
        user.save(using=self._db)

    def create_superuser(self, email, password, registration_date, **kwargs):
        user = self.model(
            email=email,
            registration_date=timezone.now(),
            is_staff=True,
            is_superuser=True,
            is_active=True,
            **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
