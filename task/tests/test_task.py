from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from task.models import Task, TaskStatus, TaskImage


User = get_user_model()


class TaskModelTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

        cls.status = TaskStatus.objects.create(
            name='Open'
        )

        cls.task = Task.objects.create(
            title='Test Task',
            description='Test Task Description',
            author=cls.user,
            status=cls.status,
        )

        cls.task.assignee.add(cls.user)

        cls.task_image = TaskImage.objects.create(
            task=cls.task,
            image='test_image.jpg'
        )

    def test_task_model(self):
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'Test Task Description')
        self.assertEqual(task.author, self.user)
        self.assertEqual(task.status, self.status)

    def test_task_str(self):
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(str(task), 'Task for testuser Test Task')

    def test_task_assignee(self):
        task = Task.objects.get(id=self.task.id)
        self.assertIn(self.user, task.assignee.all())

    def test_task_image(self):
        task_image = TaskImage.objects.get(id=self.task_image.id)
        self.assertEqual(task_image.image, 'test_image.jpg')
