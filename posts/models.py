from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models


class PostTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.body[:50]


class Post(PostTemplate):
    title = models.CharField(max_length=255)
    campaign = models.ForeignKey('campaign.Campaign', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={
            'post_pk': self.pk
            })

    def comments(self):
        return Comment.objects.filter(post=self).order_by('date')

class Comment(PostTemplate):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)