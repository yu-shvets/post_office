from django.shortcuts import render, HttpResponseRedirect, render_to_response
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from .models import Posts
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .serializers import PostSerializer
from rest_framework import generics
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly

# Getting custom User
User = get_user_model()


# Creating form inherited from model
class PostForm(ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'post']


def index(request):

    # Getting the list of Post objects
    posts = Posts.objects.all()

    paginator = Paginator(posts, 3)  # Show 3 contacts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'posts': posts})


# View for publishing a new post
def newpost(request):

    newpostform = PostForm(data=request.POST)

    if newpostform.is_valid():
        newpost = newpostform.save(commit=False)
        newpost.user = User.objects.get(id=request.user.id)
        newpost.save()

        newpostform = PostForm()

    posts = Posts.objects.all()

    return render(request, 'newpost.html', {'form': newpostform, 'posts': posts})


# View for getting a list of specified user
def userlist(request, user_id):

    posts = Posts.objects.filter(user=user_id)

    return render(request, 'userlist.html', {'posts': posts})


# View for search
def search(request):

    if 'query' in request.GET and request.GET['query'].strip():
        query = request.GET['query'].strip()
        posts = Posts.objects.filter(post__icontains=query)

        return render_to_response('search_result.html', {'posts': posts, 'query': query})

    else:
        return HttpResponseRedirect('%s?search_message=Please, submit a search term' % reverse('home'))


# REST API
class PostList(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
