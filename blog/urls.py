from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'^blog/(?P<post_id>[0-9]+)/$', views.comments, name='comment_page'),
]