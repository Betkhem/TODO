from django.db import models
from django.contrib.auth.models import User


class TaskStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class TaskImage(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='images')


class Task(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField()
    assignee = models.ManyToManyField(User)
    image = models.ManyToManyField(TaskImage, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, related_name='task_author')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(TaskStatus, default=1, on_delete=models.SET_DEFAULT)

    def __str__(self):
        return f"Task for {', '.join(self.assignee.values_list('username', flat=True))} {self.title}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, related_name='comment_author')
    text = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.author} commented:\n {self.text}"
