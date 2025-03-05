from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following", blank=True)

    def follow(self, user):
        if user != self:
            self.following.add(user)

    def unfollow(self, user):
        if user in self.following.all():
            self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(id=user.id).exists()

    def followers_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()
    
    def __str__(self):
        return self.username

    def is_admin(self):
        """Check if user is admin or not"""
        admin_emails = ["omnoi123p@gmail.com"]  # ✅ Add your admin email(s) here
        return self.email in admin_emails

