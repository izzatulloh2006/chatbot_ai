from django.db import models


class User(models.Model):
    user_id =  models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    first_name  = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username or self.user_id}"


class Question(models.Model):
    user_id = models.BigIntegerField()
    username = models.CharField(max_length=150, blank=True, null=True)
    question = models.TextField()
    answer = models.TextField()
    language = models.CharField(max_length=10, default="uz")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username or self.user_id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"