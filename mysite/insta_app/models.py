from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import CharField
from phonenumber_field.modelfields import PhoneNumberField



class UserProfile(AbstractUser):
    username = CharField(max_length=50, unique=True)
    user_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    user_network = models.URLField(null=True, blank=True)
    date_registered = models.DateField(auto_now_add=True)
    phone_number = PhoneNumberField( null=True, blank=True,
        unique=True)

    def __str__(self):
        return self.username


    def followers_count(self):
        return self.following_set.count()


    def following_count(self):
        return self.follower_set.count()


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='follower_set')
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='following_set')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


class Hashtag(models.Model):
    hashtag_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.hashtag_name


class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts')
    music = models.FileField(upload_to='music/', null=True, blank=True)
    hashtag = models.ManyToManyField(Hashtag, blank=True, related_name='posts')
    description = models.TextField(null=True, blank=True)
    people = models.ManyToManyField(UserProfile, blank=True, related_name='tagged_posts')
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f" {self.user} ,{self.created_date}"


    def likes_count(self):
        return self.post_likes.filter(like=True).count()


    def comments_count(self):
        return self.comments.count()


class Content(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='contents')
    file = models.FileField(upload_to='post_contents/')



class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    like = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post',)




class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


    def likes_count(self):
        return self.comment_likes.filter(like=True).count()


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comment_likes')
    like = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment',)


class SavePost(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='saved_posts')
    created_date = models.DateTimeField(auto_now_add=True)




class SavePostItem(models.Model):
    save_post = models.ForeignKey(SavePost, on_delete=models.CASCADE, related_name='items')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved_by')
    created_date = models.DateTimeField(auto_now_add=True)



class Stories(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='stories')
    file = models.FileField(upload_to='stories/')
    created_date = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_date = models.DateTimeField(auto_now_add=True)

class Messege(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    authot = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image =models.ImageField(upload_to='image')
    video = models.FileField(upload_to='video', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
