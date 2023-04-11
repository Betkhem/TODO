from rest_framework.serializers import ModelSerializer
from .models import Task, Comment, TaskStatus


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class TaskSerilaizer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskStatusSerializer(ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = '__all__'
