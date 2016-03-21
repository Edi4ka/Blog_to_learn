from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'^blog/(?P<post_id>[0-9]+)/$', views.comments, name='comment_page'),
    url(r'blog/registration/$', views.registration_form, name='registration'),
    url(r'blog/registration_success/$', views.registration_success, name='registration_successful'),
    url(r'^blog/logout/$', 'django.contrib.auth.views.logout', {"next_page": "/"}),
    url(r'^blog/login/$', views.login_user, name='login'),
    url(r'^blog/add_post/$', views.add_post, name='add_post'),
    url(r'^blog/edit_comment/(?P<comment_id>[0-9]+)/$', views.edit_comment, name='edit_comment'),
    url(r'blog/delete_comment/(?P<comment_id>[0-9]+)/$', views.delete_comment, name='delete_comment'),
    url(r'^blog/edit_post/(?P<post_id>[0-9]+)/$', views.edit_post, name='edit_post'),
    url(r'^blog/delete_post/(?P<post_id>[0-9]+)/$', views.delete_post, name='delete_post'),
    url(r'^blog/personal/(?P<username>[\w]+)/$', views.personal, name='personal'),
    url(r'^blog/personal/approve/(?P<post_id>[0-9]+)/$', views.approve_post, name='approve_post'),
    url(r'^blog/add_plus_post/(?P<post_id>[0-9]+)/$', views.add_plus_post, name='add_plus_post'),
    url(r'^blog/add_minus_post/(?P<post_id>[0-9]+)/$', views.add_minus_post, name='add_minus_post'),
    url(r'^blog/add_plus_comment/(?P<comment_id>[0-9]+)/$', views.add_plus_comment, name='add_plus_comment'),
    url(r'^blog/add_minus_comment/(?P<comment_id>[0-9]+)/$', views.add_minus_comment, name='add_minus_comment'),
    url(r'^blog/main_info/$', views.main_info, name='main_info'),
]
