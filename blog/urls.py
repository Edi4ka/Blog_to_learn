from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'^blog/(?P<post_id>[0-9]+)/$', views.comments, name='comment_page'),
    url(r'blog/registration/$', views.registration_form, name='registration'),
    url(r'blog/registration_success/$', views.registration_success, name='registration_successful'),
    url(r'^blog/logout/$', 'django.contrib.auth.views.logout', {"next_page": "/"}),
    url(r'^blog/login/$', views.login_user, name='login')
]