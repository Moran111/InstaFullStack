from django.db import models
from imagekit.models import ProcessedImageField
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.
# custome user model add profile picture , extends abstract user
class InstaUser(AbstractUser):
    #upload personal picture
    profile_pic = ProcessedImageField(
        upload_to='static/images/profiles',
        format='JPEG',
        options={'quality':100},
        blank=True,
        null=True
        )

    def get_connections(self):
        connections = UserConnection.objects.filter(creator=self)
        return connections

    def get_followers(self):
        followers = UserConnection.objects.filter(following=self)
        return followers

    def is_followed_by(self, user):
        followers = UserConnection.objects.filter(following=self)
        return followers.filter(creator=user).exists()
    # get url and update it
    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])

    def __str__(self):
        return self.username


class UserConnection(models.Model):
    #automated generate datetime
    created = models.DateTimeField(auto_now_add=True, editable=False)
    # creator is a instauser
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set")
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set")

    def __str__(self):
        return self.creator.username + ' follows ' + self.following.username


class Post(models.Model):
    # it should be a fk beucase it indicate a InstaUser
    author = models.ForeignKey( # a foreign key indicate a Many-To-One relationship
        InstaUser, #foreign key is InstaUser
        blank=True,
        null=True,
        on_delete=models.CASCADE, # delete this author will delete all his posts
        related_name='posts', # we can use author.posts to get all posts belong to this user
        )
    title = models.TextField(blank=True, null=True)
    image = ProcessedImageField(
        upload_to='static/images/posts',
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True,
        )

    posted_on = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    def get_like_count(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.id)])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',)
    user = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.comment


# like link post and user, which user likes which post? is a relational model
class Like(models.Model):
    # A like post1, when the post1 is delete, the like will be deleted together
    # each like is an object, related_name=likes means, post1.likes can find all user who like
    # posts1
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes',)
    # field user indicate InstaUser Model
    user = models.ForeignKey(InstaUser, on_delete=models.CASCADE)

    # one user just can like one post
    class Meta:
        unique_together = ("post", "user")
    # show in db, post1 like user1
    def __str__(self):
        return 'Like: ' + self.user.username + ' ' + self.post.title
