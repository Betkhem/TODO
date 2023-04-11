from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from task.models import Task, TaskStatus, Comment
from task.serializers import CommentSerializer


class TaskViewsTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.task_status = TaskStatus.objects.create(name='Test')
        self.task = Task.objects.create(
            title='Test task',
            description='Test description',
            author=self.user,
            status=self.task_status
        )
        self.comment_data = {'text': 'Test Comment', 'task': self.task.id, 'author': self.user.pk}

    def test_create_task(self):
        url = reverse('all-task-board_create-task')
        data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'author': self.user.pk,
            'assignee': [self.user.pk],
            'status': self.task_status.pk,
            'image': []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Task')
        self.assertEqual(response.data['description'], 'This is a test task')
        self.assertEqual(response.data['status'], self.task_status.pk)
        self.assertEqual(response.data['image'], [])
        self.assertEqual(response.data['assignee'], [self.user.pk])
        self.assertEqual(response.data['author'], self.user.pk)

    def test_update_task(self):
        url = reverse('delete-update-task', args=[self.task.id])
        new_title = "New title"
        new_description = 'New description'
        data = {
            'pk': self.task.pk,
            'title': new_title,
            'description': new_description,
            'assignee': [self.user.pk]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], new_title)
        self.assertEqual(response.data['description'], new_description)

    def test_delete_task(self):
        url = reverse('delete-update-task', args=[self.task.id])
        new_title = "New title"
        new_description = 'New description'
        data = {
            'pk': self.task.pk,
            'title': new_title,
            'description': new_description,
            'assignee': [self.user.pk]
        }
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_task_list_by_status_view(self):
        url = reverse('all-task-board_create-task')
        data = {'status': "Test"}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.task.title)

    def test_create_comment(self):
        url = reverse('all-comments_create-comment')
        self.client.force_login(self.user)
        response = self.client.post(url, data=self.comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().text, 'Test Comment')

    def test_get_comment_list(self):
        url = reverse('all-comments_create-comment')
        Comment.objects.create(text='Test Comment 1', task=self.task, author=self.user)
        Comment.objects.create(text='Test Comment 2', task=self.task, author=self.user)
        response = self.client.get(url)
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_comment_by_id(self):
        comment = Comment.objects.create(text='Test Comment', task=self.task, author=self.user)
        url = reverse('comment_retrieve_destroy_update', kwargs={'pk': comment.pk})
        response = self.client.get(url)
        serializer = CommentSerializer(comment)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_comment(self):
        comment = Comment.objects.create(text='Test Comment', task=self.task, author=self.user)
        url = reverse('comment_retrieve_destroy_update', kwargs={'pk': comment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)
