"""
URL patterns for the views included in ``django.contrib.auth``.

Including these URLs (via the ``include()`` directive) will set up
these patterns based at whatever URL prefix they are included under.

The URLconfs in the built-in django_registration workflows already have an
``include()`` for these URLs, so if you're using one of them it is not
necessary to manually include these views.

"""

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from devday.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm

urlpatterns = [
    url(r'^login/$',
        auth_views.login,
        {'template_name': 'django_registration/login.html',
         'authentication_form': AuthenticationForm},
        name='auth_login'),
    url(r'^logout/$',
        auth_views.logout,
        {'template_name': 'django_registration/logout.html'},
        name='auth_logout'),
    url(r'^password/change/$',
        auth_views.password_change,
        {'post_change_redirect': 'auth_password_change_done',
         'template_name': 'django_registration/password_change_form.html',
         'password_change_form': PasswordChangeForm},
        name='auth_password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        {'template_name': 'django_registration/password_change_done.html'},
        name='auth_password_change_done'),
    url(r'^password/reset/$',
        auth_views.password_reset,
        {'post_reset_redirect': 'auth_password_reset_done',
         'template_name': 'django_registration/password_reset_form.html',
         'password_reset_form': PasswordResetForm,
         'email_template_name': 'django_registration/password_reset_email.txt'},
        name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'post_reset_redirect': 'auth_password_reset_complete',
         'template_name': 'django_registration/password_reset_confirm.html',
         'set_password_form': SetPasswordForm},
        name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        {'template_name': 'django_registration/password_reset_complete.html'},
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        {'template_name': 'django_registration/password_reset_done.html'},
        name='auth_password_reset_done'),
]
