"""post_office URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from posts.views import index, newpost, userlist, search
from django.views.generic.base import RedirectView, TemplateView
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from cuser.forms import AuthenticationForm
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required

urlpatterns = [

    url(r'^accounts/login/$', login, {'authentication_form': AuthenticationForm}, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, kwargs={'next_page': 'home'},
        name='auth_logout'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'),
        name='registration_complete'),
    url(r'^accounts/', include('registration.backends.simple.urls',
        namespace='accounts')),
    url(r'^users/profile/$', login_required(TemplateView.as_view(
        template_name='registration/profile.html')), name='profile'),

    url(r'^$', index, name='home'),

    url(r'^newpost/$', login_required(newpost), name='newpost'),

    url(r'^users/(?P<user_id>\d+)/$', userlist, name='userlist'),

    url(r'^search_result/$', search, name='search'),

    url(r'^admin/', admin.site.urls),
]
