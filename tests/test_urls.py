from django.test import TestCase
from django.urls import reverse, resolve
from join_backend.views import set_csrf_token, LoginView, UserRegistrationView, UserDetailsView, ContactListCreateView, ContactDetailView, CategoryListCreateAPIView, CategoryDetailAPIView, SubtaskListCreateAPIView, SubtaskDetailAPIView, TaskListCreateAPIView, TaskDetailAPIView

class TestUrls(TestCase):

    def test_set_csrf_url(self):
        url = reverse('set-csrf')
        self.assertEqual(resolve(url).func, set_csrf_token)

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_signup_url(self):
        url = reverse('user-register')
        self.assertEqual(resolve(url).func.view_class, UserRegistrationView)

    def test_user_details_url(self):
        url = reverse('user-details')
        self.assertEqual(resolve(url).func.view_class, UserDetailsView)

    def test_add_contact_url(self):
        url = reverse('add_contact')
        self.assertEqual(resolve(url).func.view_class, ContactListCreateView)

    def test_contact_detail_url(self):
        url = reverse('contact_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, ContactDetailView)

    def test_category_list_url(self):
        url = reverse('category-list')
        self.assertEqual(resolve(url).func.view_class, CategoryListCreateAPIView)

    def test_category_detail_url(self):
        url = reverse('category-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, CategoryDetailAPIView)

    def test_subtask_list_url(self):
        url = reverse('subtask-list')
        self.assertEqual(resolve(url).func.view_class, SubtaskListCreateAPIView)

    def test_subtask_detail_url(self):
        url = reverse('subtask-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, SubtaskDetailAPIView)

    def test_task_list_url(self):
        url = reverse('task-list')
        self.assertEqual(resolve(url).func.view_class, TaskListCreateAPIView)

    def test_task_detail_url(self):
        url = reverse('task-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, TaskDetailAPIView)
