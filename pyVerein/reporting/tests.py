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
import itertools

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
        user.name = 'temp_last'
        user.save()

        user2 = User.objects.create_user('temp2', 'temp2@temp.tld', 'temp2pass')
        user2.first_name = 'temp2_first'
        user2.name = 'temp2_last'
        user2.save()

        group = Group.objects.create(name='group').save()
        group2 = Group.objects.create(name='group2').save()

        # login with user
        self.client.login(username='temp', password='temppass')

        with self.settings(MEDIA_ROOT=self.temp_dir):
            # Create report
            report = Report.objects.create(name='testreport', model='MEM', jsonql_query='reports', report=SimpleUploadedFile('report.jrxml', bytes('Test', 'utf-8')))
            report.save()

    def test_get_report_path(self):
        "Reports should be located at 'protected/reports/{report-uuid}/definition/{resourcename}'"

        report = Report.objects.get(name='testreport')
        self.assertEqual(get_report_path(report, 'myFileName'), "protected/reports/{}/definition/{}".format(report.uuid, 'myFileName'))

    def test_get_resource_path(self):
        "Resources should be located at 'protected/reports/{report-uuid}/resource/{resourcename}'"

        with self.settings(MEDIA_ROOT=self.temp_dir):
            # Create resource
            resource = Resource.objects.create(report=Report.objects.get(name='testreport'), resource=SimpleUploadedFile('resource.txt', bytes('Test', 'utf-8')))
            resource.save()

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

    def test_report_download_data_permission(self):
        "User should only be able to download data if view_report and download_data permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('reporting:download_data'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_report'))
        response = self.client.get(reverse('reporting:download_data'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_report'))
        user.user_permissions.add(Permission.objects.get(codename='download_data'))
        response = self.client.get(reverse('reporting:download_data'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_report'))
        response = self.client.get(reverse('reporting:download_data'))
        self.assertEqual(response.status_code, 200)
    
    def test_report_data_download_model_permission(self):
        "User should only be able to download data if according permission is set"

        user = User.objects.get(username='temp')
        user.user_permissions.add(Permission.objects.get(codename='view_report'))
        user.user_permissions.add(Permission.objects.get(codename='download_data'))

        permissions = [
            'download_member_data',
            'download_division_data',
            'download_subscription_data',
            'download_account_data',
            'download_costcenter_data',
            'download_costobject_data',
            'download_transaction_data',
            'download_closuretransaction_data',
            'download_closurebalance_data'
        ]

        permissionmap = {
            'MEM': 'download_member_data',
            'DIV': 'download_division_data',
            'SUB': 'download_subscription_data',
            'ACC': 'download_account_data',
            'COC': 'download_costcenter_data',
            'COO': 'download_costobject_data',
            'TRA': 'download_transaction_data',
            'CTR': 'download_closuretransaction_data',
            'CBA': 'download_closurebalance_data'
        }


        for model in permissionmap:
            response = self.client.post(reverse('reporting:download_data'), {'models': model, 'records': 'all'})
            self.assertEqual(response.status_code, 403)

            for permission in permissions:
                p = Permission.objects.get(codename=permission)
                user.user_permissions.add(p)
                response = self.client.post(reverse('reporting:download_data'), {'models': model, 'records': 'all'})
                self.assertEqual(response.status_code, 200 if permission == permissionmap[model] else 403)

                user.user_permissions.remove(p)
    
    def test_report_resource_upload_permission(self):
        "User should only be able to upload resources if permission is set"
        with self.settings(MEDIA_ROOT=self.temp_dir):
            user = User.objects.get(username='temp')
            
            response = self.client.post(reverse('reporting:upload_resource', args={Report.objects.get(name='testreport').pk}), {'resource': SimpleUploadedFile('Testresource.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 403)

            user.user_permissions.add(Permission.objects.get(codename='view_report'))
            response = self.client.post(reverse('reporting:upload_resource', args={Report.objects.get(name='testreport').pk}), {'resource': SimpleUploadedFile('Testresource.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 403)

            user.user_permissions.remove(Permission.objects.get(codename='view_report'))
            user.user_permissions.add(Permission.objects.get(codename='change_report'))
            response = self.client.post(reverse('reporting:upload_resource', args={Report.objects.get(name='testreport').pk}), {'resource': SimpleUploadedFile('Testresource.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 403)

            user.user_permissions.add(Permission.objects.get(codename='view_report'))
            response = self.client.post(reverse('reporting:upload_resource', args={Report.objects.get(name='testreport').pk}), {'resource': SimpleUploadedFile('Testresource.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 200)

    def test_report_resource_delete_permission(self):
        with self.settings(MEDIA_ROOT=self.temp_dir):
            "User should only be able to delete resources if permission is set"
            user = User.objects.get(username='temp')
            user.user_permissions.add(Permission.objects.get(codename='view_report'))
            user.user_permissions.add(Permission.objects.get(codename='change_report'))
            self.client.post(reverse('reporting:upload_resource', args={Report.objects.get(name='testreport').pk}), {'resource': SimpleUploadedFile('Testresource.txt', bytes('Test', 'utf-8'))})
            user.user_permissions.remove(Permission.objects.get(codename='view_report'))
            user.user_permissions.remove(Permission.objects.get(codename='change_report'))

                    
            response = self.client.post(reverse('reporting:delete_resource', args={Resource.objects.filter(report=Report.objects.get(name='testreport')).first().pk}))
            self.assertEqual(response.status_code, 403)

            user.user_permissions.add(Permission.objects.get(codename='view_report'))
            response = self.client.post(reverse('reporting:delete_resource', args={Resource.objects.filter(report=Report.objects.get(name='testreport')).first().pk}))
            self.assertEqual(response.status_code, 403)

            user.user_permissions.remove(Permission.objects.get(codename='view_report'))
            user.user_permissions.add(Permission.objects.get(codename='change_report'))
            response = self.client.post(reverse('reporting:delete_resource', args={Resource.objects.filter(report=Report.objects.get(name='testreport')).first().pk}))
            self.assertEqual(response.status_code, 403)

            user.user_permissions.add(Permission.objects.get(codename='view_report'))
            response = self.client.post(reverse('reporting:delete_resource', args={Resource.objects.filter(report=Report.objects.get(name='testreport')).first().pk}))
            self.assertEqual(response.status_code, 302)
    
    def test_report_resource_download_permission(self):
        with self.settings(MEDIA_ROOT=self.temp_dir):
            "User should only be able to download resources if permission is set"
            user = User.objects.get(username='temp')
            user.user_permissions.add(Permission.objects.get(codename='view_report'))
            user.user_permissions.add(Permission.objects.get(codename='change_report'))
            self.client.post(reverse('reporting:upload_resource', args={Report.objects.get(name='testreport').pk}), {'resource': SimpleUploadedFile('Testresource.txt', bytes('Test', 'utf-8'))})
            user.user_permissions.remove(Permission.objects.get(codename='view_report'))
            user.user_permissions.remove(Permission.objects.get(codename='change_report'))

                    
            response = self.client.get(reverse('reporting:download_resource', args={Resource.objects.filter(report=Report.objects.get(name='testreport')).first().pk}))
            self.assertEqual(response.status_code, 403)

            user.user_permissions.add(Permission.objects.get(codename='view_report'))
            response = self.client.get(reverse('reporting:download_resource', args={Resource.objects.filter(report=Report.objects.get(name='testreport')).first().pk}))
            self.assertEqual(response.status_code, 200)

    def test_report_upload_resource_access_restrictions(self):
        "User should only be able to upload resources if user is not restricted to access the assigned report"
        with self.settings(MEDIA_ROOT=self.temp_dir):
            user = User.objects.get(username='temp')    
            user.user_permissions.add(Permission.objects.get(codename='view_report'))
            user.user_permissions.add(Permission.objects.get(codename='change_report'))
            self.client.post(reverse('reporting:upload_resource', args={Report.objects.get(name='testreport').pk}), {'resource': SimpleUploadedFile('Testresource.txt', bytes('Test', 'utf-8'))})
            report = Report.objects.get(name='testreport')
            user2 = User.objects.get(username='temp2')
            group = Group.objects.get(name='group')
            group2 = Group.objects.get(name='group2')

            # Access restrictions for user
            report.user.add(user2)
            response = self.client.post(reverse('reporting:upload_resource', args={Report.objects.get(name='testreport').pk}), {'resource': SimpleUploadedFile('Testresource.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 403)

            report.user.add(user)
            response = self.client.post(reverse('reporting:upload_resource', args={Report.objects.get(name='testreport').pk}), {'resource': SimpleUploadedFile('Testresource.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 200)

            report.user.remove(user)
            report.user.remove(user2)

            # Access restrictions for groups
            group.user_set.add(user)
            group2.user_set.add(user2)

            report.groups.add(group2)
            response = self.client.post(reverse('reporting:upload_resource', args={Report.objects.get(name='testreport').pk}), {'resource': SimpleUploadedFile('Testresource.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 403)

            report.groups.add(group)
            response = self.client.post(reverse('reporting:upload_resource', args={Report.objects.get(name='testreport').pk}), {'resource': SimpleUploadedFile('Testresource.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 200)
        
    def test_report_download_resource_access_restrictions(self):
        "User should only be able to download resources if user is not restricted to access the assigned report"
        with self.settings(MEDIA_ROOT=self.temp_dir):
            user = User.objects.get(username='temp')    
            user.user_permissions.add(Permission.objects.get(codename='view_report'))
            user.user_permissions.add(Permission.objects.get(codename='change_report'))
            self.client.post(reverse('reporting:upload_resource', args={Report.objects.get(name='testreport').pk}), {'resource': SimpleUploadedFile('Testresource.txt', bytes('Test', 'utf-8'))})
            report = Report.objects.get(name='testreport')
            user2 = User.objects.get(username='temp2')
            group = Group.objects.get(name='group')
            group2 = Group.objects.get(name='group2')

            # Access restrictions for user
            report.user.add(user2)
            response = self.client.get(reverse('reporting:download_resource', args={Resource.objects.filter(report=Report.objects.get(name='testreport')).first().pk}))
            self.assertEqual(response.status_code, 403)

            report.user.add(user)
            response = self.client.get(reverse('reporting:download_resource', args={Resource.objects.filter(report=Report.objects.get(name='testreport')).first().pk}))
            self.assertEqual(response.status_code, 200)

            report.user.remove(user)
            report.user.remove(user2)

            # Access restrictions for groups
            group.user_set.add(user)
            group2.user_set.add(user2)

            report.groups.add(group2)
            response = self.client.get(reverse('reporting:download_resource', args={Resource.objects.filter(report=Report.objects.get(name='testreport')).first().pk}))
            self.assertEqual(response.status_code, 403)

            report.groups.add(group)
            response = self.client.get(reverse('reporting:download_resource', args={Resource.objects.filter(report=Report.objects.get(name='testreport')).first().pk}))
            self.assertEqual(response.status_code, 200)

    def test_report_delete_resource_access_restrictions(self):
        "User should only be able to delete resources if user is not restricted to access the assigned report"
        with self.settings(MEDIA_ROOT=self.temp_dir):
            user = User.objects.get(username='temp')    
            user.user_permissions.add(Permission.objects.get(codename='view_report'))
            user.user_permissions.add(Permission.objects.get(codename='change_report'))
            self.client.post(reverse('reporting:upload_resource', args={Report.objects.get(name='testreport').pk}), {'resource': SimpleUploadedFile('Testresource.txt', bytes('Test', 'utf-8'))})
            report = Report.objects.get(name='testreport')
            user2 = User.objects.get(username='temp2')
            group = Group.objects.get(name='group')
            group2 = Group.objects.get(name='group2')

            # Access restrictions for user
            report.user.add(user2)
            response = self.client.post(reverse('reporting:delete_resource', args={Resource.objects.filter(report=Report.objects.get(name='testreport')).first().pk}))
            self.assertEqual(response.status_code, 403)

            report.user.add(user)
            response = self.client.post(reverse('reporting:delete_resource', args={Resource.objects.filter(report=Report.objects.get(name='testreport')).first().pk}))
            self.assertEqual(response.status_code, 302)

            report.user.remove(user)
            report.user.remove(user2)

            # Access restrictions for groups
            group.user_set.add(user)
            group2.user_set.add(user2)
            self.client.post(reverse('reporting:upload_resource', args={Report.objects.get(name='testreport').pk}), {'resource': SimpleUploadedFile('Testresource.txt', bytes('Test', 'utf-8'))})
            
            report.groups.add(group2)
            response = self.client.post(reverse('reporting:delete_resource', args={Resource.objects.filter(report=Report.objects.get(name='testreport')).first().pk}))
            self.assertEqual(response.status_code, 403)

            report.groups.add(group)
            response = self.client.post(reverse('reporting:delete_resource', args={Resource.objects.filter(report=Report.objects.get(name='testreport')).first().pk}))
            self.assertEqual(response.status_code, 302)
