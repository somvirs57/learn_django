from django.db import models
from taggit.managers import TaggableManager

# Create your models here.
class IpModel(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip

class Blog(models.Model):
    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=550)
    tags = TaggableManager()
    views = models.ManyToManyField(IpModel, related_name="post_views", blank=True)
    likes = models.ManyToManyField(IpModel, related_name="post_likes", blank=True)


    def __str__(self):
        return self.title

    def total_views(self):
        return self.views.count()

    def total_likes(self):
        return self.likes.count()
