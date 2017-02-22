from django.conf.urls import url, include
from posts import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url(r'^api/posts/$', views.PostList.as_view()),
    url(r'^api/posts/(?P<pk>[0-9]+)/$', views.PostDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^api-token-auth/', obtain_auth_token),

]
