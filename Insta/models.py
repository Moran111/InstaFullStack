from django.db import models
from imagekit.models import ProcessedImageField
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.
# custome use model add profile picture , extends abstract user
class InstaUser(AbstractUser):
    # personal image picture, upload to profiles
    profile_pic = ProcessedImageField(
        upload_to='static/images/profiles',
        format='JPEG',
        options={'quality': 100},
        null=True,
        blank=True,
        )

        

class Post(models.Model):
    # it should be a fk beucase it indicate a InstaUser
    author = models.ForeignKey( # a foreign key indicate a Many-To-One relationship
        InstaUser, #foreign key is InstaUser
        blank=True,
        null=True,
        on_delete=models.CASCADE, # delete this author will delete all his posts
        related_name='my_posts', # i can use myposts to find all my posts
        )
    title = models.TextField(blank=True, null=True)
    image = ProcessedImageField (
        upload_to='static/images/posts',
        format='JPEG',
        options={'quality':100},
        blank=True,
        null=True
    )

    def get_absolute_url(self):
        return reverse("post_detail",args=[str(self.id)])

    def get_like_count(self):
        return self.likes.count()

    def get_comment_count(self):
        return self.comments.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',)
    user = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.comment

# like link post and user, which user likes which post? is a relational model
class Like(models.Model):
    # A like post1, when the post is delete, the like will be deleted together
    # when post1 is deleted, the like will disappear
    # each like is an object, related_name=likes means, post1.likes can find all user who like
    # posts1
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes',)
    # field user indicate InstaUser Model
    user = models.ForeignKey(InstaUser, on_delete=models.CASCADE, related_name='likes')

    # one user just can like one post
    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return 'Like: ' + self.user.username + ' ' + self.post.title
