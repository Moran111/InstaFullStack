from annoying.decorators import ajax_request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from Insta.forms import CustomUserCreationForm
from Insta.models import InstaUser, Like, Post, UserConnection, Comment

# class based view
class HelloWorld(TemplateView):
    template_name = 'test.html'

class PostsView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'index.html'
    login_url = 'login'

    def get_queryset(self):
        current_user = self.request.user
        following = set()
        for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
            following.add(conn.following)
        return Post.objects.filter(author__in=following)

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = '__all__'
    login_url = 'login'

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title']

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy("posts")

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy("login")

class UserDetailView(LoginRequiredMixin, DetailView):
    model = InstaUser
    template_name = 'user_detail.html'
    login_url = 'login'

# can be edit from user detail
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = InstaUser
    template_name = 'edit_profile.html'
    fields = ['profile_pic', 'username']
    login_url = 'login'
    success_url = reverse_lazy("posts")

class ExploreView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'explore.html'
    login_url = 'login'

    def get_queryset(self):
        return Post.objects.all().order_by('-posted_on')[:20]


# non class based view
@ajax_request
def toggleFollow(request):
    current_user = InstaUser.objects.get(pk=request.user.pk)
    follow_user_pk = request.POST.get('follow_user_pk')
    follow_user = InstaUser.objects.get(pk=follow_user_pk)

    try:
        if current_user != follow_user:
            if request.POST.get('type') == 'follow':
                connection = UserConnection(creator=current_user, following=follow_user)
                connection.save()
            elif request.POST.get('type') == 'unfollow':
                UserConnection.objects.filter(creator=current_user, following=follow_user).delete()
            result = 1
        else:
            result = 0
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'type': request.POST.get('type'),
        'follow_user_pk': follow_user_pk
    }

# @ajax_request means the def addLike(request) only response to ajax's request
@ajax_request
# can get json format data(post's pk) from index.js create_like request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    # which post i click like?
    post = Post.objects.get(pk=post_pk)
    try:
        # Like is a contstructor
        like = Like(post=post, user=request.user)
        # save like object to db, if i found same like has already exist in the db
        like.save()
        result = 1
    except Exception as e:
        #  delete like
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }

@ajax_request
def addComment(request):
    comment_text = request.POST.get('comment_text')
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    commenter_info = {}

    try:
        comment = Comment(comment=comment_text, user=request.user, post=post)
        comment.save()

        username = request.user.username

        commenter_info = {
            'username': username,
            'comment_text': comment_text
        }

        result = 1
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }
