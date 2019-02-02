from django.test import TestCase
from account.models import User
from django.urls import reverse
from django.contrib.auth.models import Permission

class TasksTestMethods(TestCase):
    def setUp(self):
        # Create user
        user = User.objects.create_user('temp', 'temp@temp.tld', 'temppass')
        user.first_name = 'temp_first'
        user.last_name = 'temp_last'
        user.save()

        # login with user
        self.client.login(username='temp', password='temppass')

    def test_task_list_permission(self):
        "User should only access task list if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('tasks:task_list'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_tasks'))
        response = self.client.get(reverse('tasks:task_list'))
        self.assertEqual(response.status_code, 200)

    def test_run_subscription_task_permission(self):
        "User should only access subscription task if view, run and subscription_task permissions are set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('tasks:apply_subscriptions'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_tasks'))
        response = self.client.get(reverse('tasks:apply_subscriptions'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_tasks'))
        response = self.client.get(reverse('tasks:apply_subscriptions'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_subscription_task'))
        response = self.client.get(reverse('tasks:apply_subscriptions'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='run_subscription_task'))
        user.user_permissions.add(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_tasks'))
        response = self.client.get(reverse('tasks:apply_subscriptions'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.remove(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_subscription_task'))
        response = self.client.get(reverse('tasks:apply_subscriptions'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.remove(Permission.objects.get(codename='run_subscription_task'))
        user.user_permissions.add(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_subscription_task'))
        response = self.client.get(reverse('tasks:apply_subscriptions'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.remove(Permission.objects.get(codename='run_subscription_task'))
        user.user_permissions.add(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_subscription_task'))
        response = self.client.get(reverse('tasks:apply_subscriptions'))
        self.assertEqual(response.status_code, 400)

    def test_run_closure_task_permission(self):
        "User should only access closure task if view, run and closure_task permissions are set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('tasks:apply_annualclosure'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_tasks'))
        response = self.client.get(reverse('tasks:apply_annualclosure'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_tasks'))
        response = self.client.get(reverse('tasks:apply_annualclosure'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_closure_task'))
        response = self.client.get(reverse('tasks:apply_annualclosure'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='run_closure_task'))
        user.user_permissions.add(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_tasks'))
        response = self.client.get(reverse('tasks:apply_annualclosure'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.remove(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_closure_task'))
        response = self.client.get(reverse('tasks:apply_annualclosure'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.remove(Permission.objects.get(codename='run_closure_task'))
        user.user_permissions.add(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_closure_task'))
        response = self.client.get(reverse('tasks:apply_annualclosure'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.remove(Permission.objects.get(codename='run_closure_task'))
        user.user_permissions.add(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_closure_task'))
        response = self.client.get(reverse('tasks:apply_annualclosure'))
        self.assertEqual(response.status_code, 400)
    
    def test_run_delete_terminated_members_task_permission(self):
        "User should only access delete terminated members task if view, run and delete_terminated_members_task permissions are set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('tasks:delete_terminated_members'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_tasks'))
        response = self.client.get(reverse('tasks:delete_terminated_members'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_tasks'))
        response = self.client.get(reverse('tasks:delete_terminated_members'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_delete_terminated_members_task'))
        response = self.client.get(reverse('tasks:delete_terminated_members'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='run_delete_terminated_members_task'))
        user.user_permissions.add(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_tasks'))
        response = self.client.get(reverse('tasks:delete_terminated_members'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.remove(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_delete_terminated_members_task'))
        response = self.client.get(reverse('tasks:delete_terminated_members'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.remove(Permission.objects.get(codename='run_delete_terminated_members_task'))
        user.user_permissions.add(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_delete_terminated_members_task'))
        response = self.client.get(reverse('tasks:delete_terminated_members'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.remove(Permission.objects.get(codename='run_delete_terminated_members_task'))
        user.user_permissions.add(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_delete_terminated_members_task'))
        response = self.client.get(reverse('tasks:delete_terminated_members'))
        self.assertEqual(response.status_code, 400)

    def test_run_delete_report_data_task_permission(self):
        "User should only access delete report data task if view, run and delete_report_data_task permissions are set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('tasks:delete_report_data'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_tasks'))
        response = self.client.get(reverse('tasks:delete_report_data'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_tasks'))
        response = self.client.get(reverse('tasks:delete_report_data'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_delete_report_data_task'))
        response = self.client.get(reverse('tasks:delete_report_data'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='run_delete_report_data_task'))
        user.user_permissions.add(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_tasks'))
        response = self.client.get(reverse('tasks:delete_report_data'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.remove(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_delete_report_data_task'))
        response = self.client.get(reverse('tasks:delete_report_data'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.remove(Permission.objects.get(codename='run_delete_report_data_task'))
        user.user_permissions.add(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_delete_report_data_task'))
        response = self.client.get(reverse('tasks:delete_report_data'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.remove(Permission.objects.get(codename='run_delete_report_data_task'))
        user.user_permissions.add(Permission.objects.get(codename='view_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_tasks'))
        user.user_permissions.add(Permission.objects.get(codename='run_delete_report_data_task'))
        response = self.client.get(reverse('tasks:delete_report_data'))
        self.assertEqual(response.status_code, 400)