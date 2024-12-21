from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CustomUser, Task
from .forms import TaskForm

class TaskViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')


    def test_login_view(self):
        response = self.client.post(reverse('task:login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertRedirects(response, reverse('task:tasks'))

    def test_register_view(self):
        response = self.client.post(reverse('task:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass',
            'confirmation': 'newpass'
        })
        self.assertRedirects(response, reverse('task:tasks'))

    def test_logout_view(self):
        response = self.client.get(reverse('task:logout'))
        self.assertRedirects(response, reverse('task:index'))

    def test_tasks_view(self):
        response = self.client.get(reverse('task:tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/tasks.html')

    def test_delete_task(self):
        task = Task.objects.create(author=self.user, title='Test Task')
        response = self.client.post(reverse('task:delete_task', args=[task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_new_task(self):
        response = self.client.post(reverse('task:new_task'), {'title': 'New Task', 'priority': 'important and urgent'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(title='New Task').exists())



    def test_profile_view(self):
        response = self.client.get(reverse('task:profile', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/profile.html')

    def test_edit_profile(self):
        response = self.client.post(reverse('task:edit_profile'), {
            'username': 'updateduser',
            'email': 'updateduser@example.com'
        })
        self.assertRedirects(response, reverse('task:profile', args=[self.user.id]))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updateduser@example.com')