from django.db import models
from django.conf import settings

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True, default="")
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_posts", blank=True)
    share_count = models.PositiveIntegerField(default=0)  # เพิ่ม share_count

    @property
    def type(self):
        return 'post'

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"Post by {self.user.username} on {self.created_at:%Y-%m-%d %H:%M}"

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_comments", db_index=True)
    post = models.ForeignKey(Post, related_name='comments', null=True, blank=True, on_delete=models.CASCADE)
    share = models.ForeignKey('Share', related_name='comments', null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Comments"

    def __str__(self):
        if self.post:
            return f"Comment by {self.user.username} on Post {self.post.id}"
        elif self.share:
            return f"Comment by {self.user.username} on Share {self.share.id}"
        else:
            return f"Comment by {self.user.username} (no related post or share)"

class Share(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_shares", db_index=True)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name="shares", db_index=True)
    content = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_shares", blank=True)
    image = models.ImageField(upload_to="share_images/", null=True, blank=True)
    
    @property
    def type(self):
        return 'share'

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Shares"

    def __str__(self):
        return f"{self.user.username} shared Post {self.post.id}"