from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey('auth.User')
    tags = models.SlugField()
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
