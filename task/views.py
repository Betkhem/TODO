from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from TODO.custom_permission import IsAuthorOrAdmin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerilaizer, CommentSerializer, TaskStatusSerializer
from rest_framework.permissions import IsAdminUser
from .models import Task, Comment, TaskStatus
from rest_framework.response import Response
from rest_framework import status


class TaskListCreateView(ListCreateAPIView):
    """
    List tasks or create one or filter by status
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerilaizer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_status = self.request.query_params.get('status', None)
        if filter_status is not None:
            queryset = queryset.filter(status__name=filter_status)
        return queryset

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskDestroyUpdateView(RetrieveUpdateDestroyAPIView):
    """
    Get, destroy, orr update task if author or admin
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerilaizer
    permission_classes = [IsAuthorOrAdmin]


class CommentListCreateView(ListCreateAPIView):
    """
    List or create comment
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class CommentRetrieveDestroyUpdateView(RetrieveUpdateDestroyAPIView):
    """
    Get, destroy, orr update comment if author or admin
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdmin]


class TaskStatusListCreate(ListCreateAPIView):
    """
    Get statuses or create one.
    """
    queryset = TaskStatus
    serializer_class = TaskStatusSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]


class TaskStatusRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Get status or change it if user is admin.
    """
    queryset = TaskStatus
    serializer_class = TaskStatusSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]
