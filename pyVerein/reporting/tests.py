from django.test import TestCase
from .models import Report, get_report_path, get_resource_path, Resource
from account.models import User
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from tempfile import mkdtemp
from django.conf import settings
from shutil import rmtree
from django.contrib.auth.models import Group

class ReportTestMethods(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create tempdir
        cls.temp_dir = mkdtemp()
    
    @classmethod
    def tearDownClass(self):
        super().tearDownClass()
        rmtree(self.temp_dir)

    def setUp(self):
        # Create user
        user = User.objects.create_user('temp', 'temp@temp.tld', 'temppass')
        user.first_name = 'temp_first'
        user.last_name = 'temp_last'
        user.save()

        user2 = User.objects.create_user('temp2', 'temp2@temp.tld', 'temp2pass')
        user2.first_name = 'temp2_first'
        user2.last_name = 'temp2_last'
        user2.save()

        group = Group.objects.create(name='group').save()
        group2 = Group.objects.create(name='group2').save()

        # login with user
        self.client.login(username='temp', password='temppass')

        with self.settings(MEDIA_ROOT=self.temp_dir):
            # Create report
            report = Report.objects.create(name='testreport', model='MEM', jsonql_query='members', report=SimpleUploadedFile('report.jrxml', bytes('Test', 'utf-8')))
            report.save()

            # Create resource
            resource = Resource.objects.create(report=report, resource=SimpleUploadedFile('resource.txt', bytes('Test', 'utf-8')))
            resource.save()

    def test_get_report_path(self):
        "Reports should be located at 'protected/reports/{report-uuid}/definition/{filename}'"

        report = Report.objects.get(name='testreport')
        self.assertEqual(get_report_path(report, 'myFileName'), "protected/reports/{}/definition/{}".format(report.uuid, 'myFileName'))

    def test_get_resource_path(self):
        "Resources should be located at 'protected/reports/{report-uuid}/resource/{filename}'"

        resource = Resource.objects.get(report__name='testreport')
        self.assertEqual(get_resource_path(resource, 'myFileName'), "protected/reports/{}/resource/{}".format(resource.report.uuid, 'myFileName'))

    def test_report_list_permission(self):
        "User should only access report list if view permission is set"

        user = User.objects.get(username='temp')    
        
        response = self.client.get(reverse('reporting:list'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_report'))

        response = self.client.get(reverse('reporting:list'))
        self.assertEqual(response.status_code, 200)

    def test_report_list_access_restrictions(self):
        "Report should only be listed if user is not restricted to access the report"
        
        user = User.objects.get(username='temp')    
        user.user_permissions.add(Permission.objects.get(codename='view_report'))
        report = Report.objects.get(name='testreport')
        user2 = User.objects.get(username='temp2')
        group = Group.objects.get(name='group')
        group2 = Group.objects.get(name='group2')

        # Access restrictions for user
        report.user.add(user2)
        response = self.client.get(reverse('reporting:list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'testreport')

        report.user.add(user)
        response = self.client.get(reverse('reporting:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testreport')

        report.user.remove(user)
        report.user.remove(user2)

        # Access restrictions for groups
        group.user_set.add(user)
        group2.user_set.add(user2)

        report.groups.add(group2)
        response = self.client.get(reverse('reporting:list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'testreport')

        report.groups.add(group)
        response = self.client.get(reverse('reporting:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testreport')
  
    def test_report_detail_permission(self):
        "User should only access report detail if view permission is set"

        with self.settings(MEDIA_ROOT=self.temp_dir):
            user = User.objects.get(username='temp')
            
            response = self.client.get(reverse('reporting:detail', args={Report.objects.get(name='testreport').pk}))
            self.assertEqual(response.status_code, 403)

            user.user_permissions.add(Permission.objects.get(codename='view_report'))

            response = self.client.get(reverse('reporting:detail', args={Report.objects.get(name='testreport').pk}))
            self.assertEqual(response.status_code, 200)
    
    def test_report_detail_access_restrictions(self):
        "Report detail should only be acesssable if user is not restricted to access the report"
        with self.settings(MEDIA_ROOT=self.temp_dir):
            user = User.objects.get(username='temp')   
            user.user_permissions.add(Permission.objects.get(codename='view_report'))
            report = Report.objects.get(name='testreport')
            user2 = User.objects.get(username='temp2')
            group = Group.objects.get(name='group')
            group2 = Group.objects.get(name='group2')

            # Access restrictions for user
            report.user.add(user2)
            response = self.client.get(reverse('reporting:detail', args={Report.objects.get(name='testreport').pk}))
            self.assertEqual(response.status_code, 403)

            report.user.add(user)
            response = self.client.get(reverse('reporting:detail', args={Report.objects.get(name='testreport').pk}))
            self.assertEqual(response.status_code, 200)

            report.user.remove(user)
            report.user.remove(user2)

            # Access restrictions for groups
            group.user_set.add(user)
            group2.user_set.add(user2)

            report.groups.add(group2)
            response = self.client.get(reverse('reporting:detail', args={Report.objects.get(name='testreport').pk}))
            self.assertEqual(response.status_code, 403)

            report.groups.add(group)
            response = self.client.get(reverse('reporting:detail', args={Report.objects.get(name='testreport').pk}))
            self.assertEqual(response.status_code, 200)

    def test_report_edit_permission(self):
        "User should only access report edit if change permission is set"

        with self.settings(MEDIA_ROOT=self.temp_dir):
            user = User.objects.get(username='temp')
            
            response = self.client.get(reverse('reporting:edit', args={Report.objects.get(name='testreport').pk}))
            self.assertEqual(response.status_code, 403)

            user.user_permissions.add(Permission.objects.get(codename='view_report'))
            response = self.client.get(reverse('reporting:edit', args={Report.objects.get(name='testreport').pk}))
            self.assertEqual(response.status_code, 403)

            user.user_permissions.remove(Permission.objects.get(codename='view_report'))
            user.user_permissions.add(Permission.objects.get(codename='change_report'))
            response = self.client.get(reverse('reporting:edit', args={Report.objects.get(name='testreport').pk}))
            self.assertEqual(response.status_code, 403)

            user.user_permissions.add(Permission.objects.get(codename='view_report'))
            response = self.client.get(reverse('reporting:edit', args={Report.objects.get(name='testreport').pk}))
            self.assertEqual(response.status_code, 200)
    
    def test_report_edit_access_restrictions(self):
        "Report should only be editable if user is not restricted to access the report"
        with self.settings(MEDIA_ROOT=self.temp_dir):
            user = User.objects.get(username='temp')   
            user.user_permissions.add(Permission.objects.get(codename='view_report'))
            user.user_permissions.add(Permission.objects.get(codename='change_report'))
            report = Report.objects.get(name='testreport')
            user2 = User.objects.get(username='temp2')
            group = Group.objects.get(name='group')
            group2 = Group.objects.get(name='group2')

            # Access restrictions for user
            report.user.add(user2)
            response = self.client.get(reverse('reporting:edit', args={Report.objects.get(name='testreport').pk}))
            self.assertEqual(response.status_code, 403)

            report.user.add(user)
            response = self.client.get(reverse('reporting:edit', args={Report.objects.get(name='testreport').pk}))
            self.assertEqual(response.status_code, 200)

            report.user.remove(user)
            report.user.remove(user2)

            # Access restrictions for groups
            group.user_set.add(user)
            group2.user_set.add(user2)

            report.groups.add(group2)
            response = self.client.get(reverse('reporting:edit', args={Report.objects.get(name='testreport').pk}))
            self.assertEqual(response.status_code, 403)

            report.groups.add(group)
            response = self.client.get(reverse('reporting:edit', args={Report.objects.get(name='testreport').pk}))
            self.assertEqual(response.status_code, 200)

    def test_report_create_permission(self):
        "User should only access report create if add permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('reporting:create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_report'))
        response = self.client.get(reverse('reporting:create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_report'))
        user.user_permissions.add(Permission.objects.get(codename='add_report'))
        response = self.client.get(reverse('reporting:create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_report'))
        response = self.client.get(reverse('reporting:create'))
        self.assertEqual(response.status_code, 200)
