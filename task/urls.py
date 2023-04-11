from django.urls import path
from task import views


urlpatterns = [
    path("", views.TaskListCreateView.as_view(), name='all-task-board_create-task'),
    path("<int:pk>/", views.TaskDestroyUpdateView.as_view(), name='delete-update-task'),
    path("comments/", views.CommentListCreateView.as_view(), name='all-comments_create-comment'),
    path("comments/<int:pk>/", views.CommentRetrieveDestroyUpdateView.as_view(), name='comment_retrieve_destroy_update'),
    path('statuses/', views.TaskStatusListCreate.as_view()),
    path('status/<int:pk>/', views.TaskStatusRetrieveUpdateDestroyView.as_view()),
]
