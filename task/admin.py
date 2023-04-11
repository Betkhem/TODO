from django.contrib import admin
from .models import Task, Comment, TaskStatus, TaskImage
from .forms import CommentModelForm


class CommentInline(admin.TabularInline):
    model = Comment
    form = CommentModelForm


class TaskProxy(Task):
    class Meta:
        proxy = True
        verbose_name = 'Task'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ['assignee']
    inlines = [CommentInline]


admin.site.register(TaskStatus)
admin.site.register(TaskImage)
