from django.test import TestCase
from .models import Member, Division, Subscription, File
from datetime import datetime, timedelta
from account.models import User
from django.urls import reverse
from django.contrib.auth.models import Permission, Group
from django.utils import translation
from dynamic_preferences.registries import global_preferences_registry
from shutil import rmtree
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from tempfile import mkdtemp

class MemberTestMethods(TestCase):
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

        # Create division
        division = Division.objects.create(name='Temp')
        division.save()

        # Create member
        member = Member.objects.create(salutation=Member.MR, first_name='Temp', last_name='Temp')
        member.division.add(division)
        member.save()

    # Test for get_full_name method.
    def test_get_full_name(self):
        # Create Member.
        member = Member.objects.create(first_name="first", last_name="last")

        # Assert if full name is "first last".
        self.assertEqual(member.get_full_name(), 'first last')

    # Test for is_terminated method.
    def test_is_terminated(self):
        # Create Member.
        member = Member.objects.create(first_name="first", last_name="last")

        # New member should not be terminated
        self.assertFalse(member.is_terminated())

        # Set terminated date to future value
        member.terminated_at = datetime.now().date() + timedelta(days=1)

        # Member with terminated_at date in the future should not be terminated
        self.assertFalse(member.is_terminated())

        # Set terminated date to today value
        member.terminated_at = datetime.now().date()

        # Member with terminated_at date today should be terminated
        self.assertTrue(member.is_terminated())

        # Set terminated date to past value
        member.terminated_at = datetime.now().date() - timedelta(days=1)

        # Member with terminated_at date in the past should be terminated
        self.assertTrue(member.is_terminated())

    # Test for __str__ method.
    def test__str__(self):
        # Create Member.
        member = Member.objects.create(first_name="first", last_name="last")

        # Assert if __str__ ist full name.
        self.assertEqual(str(member), "first last")

    def test_member_list_permission(self):
        "User should only access member list if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('members:member_list'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_member'))

        response = self.client.get(reverse('members:member_list'))
        self.assertEqual(response.status_code, 200)
  
    def test_member_detail_permission(self):
        "User should only access member detail if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('members:member_detail', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_member'))

        response = self.client.get(reverse('members:member_detail', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 200)

    def test_member_files_detail_permission(self):
        "User should only be able to view member files if view permission is set"

        user = User.objects.get(username='temp')
        user.user_permissions.add(Permission.objects.get(codename='view_member'))
        with translation.override('en'):
            response = self.client.get(reverse('members:member_detail', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Files')
        self.assertNotContains(response, 'Filename')
    
        user.user_permissions.add(Permission.objects.get(codename='view_files'))
        with translation.override('en'):
            response = self.client.get(reverse('members:member_detail', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Files')
        self.assertContains(response, 'Filename')

    def test_member_edit_permission(self):
        "User should only access member edit if change permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('members:member_edit', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_member'))
        response = self.client.get(reverse('members:member_edit', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_member'))
        user.user_permissions.add(Permission.objects.get(codename='change_member'))
        response = self.client.get(reverse('members:member_edit', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_member'))
        response = self.client.get(reverse('members:member_edit', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_member_create_permission(self):
        "User should only access member create if add permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('members:member_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_member'))
        response = self.client.get(reverse('members:member_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_member'))
        user.user_permissions.add(Permission.objects.get(codename='add_member'))
        response = self.client.get(reverse('members:member_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_member'))
        response = self.client.get(reverse('members:member_create'))
        self.assertEqual(response.status_code, 200)

    def test_member_field_permission(self):
        "User should only be able to see field if permission is set"

        user = User.objects.get(username='temp')
        user.user_permissions.add(Permission.objects.get(codename='view_member'))

        global_preferences_registry.manager()['Members__show_additional_field_1'] = True
        global_preferences_registry.manager()['Members__show_additional_field_2'] = True
        global_preferences_registry.manager()['Members__show_additional_field_3'] = True
        global_preferences_registry.manager()['Members__show_additional_field_4'] = True
        global_preferences_registry.manager()['Members__show_additional_field_5'] = True

        permissions = [
            'view_field_salutation',
            'view_field_last_name',
            'view_field_first_name',
            'view_field_street',
            'view_field_zipcode',
            'view_field_city',
            'view_field_birthday',
            'view_field_phone',
            'view_field_mobile',
            'view_field_fax',
            'view_field_email',
            'view_field_membership_number',
            'view_field_joined_at',
            'view_field_terminated_at',
            'view_field_division',
            'view_field_payment_method',
            'view_field_iban',
            'view_field_bic',
            'view_field_debit_mandate_at',
            'view_field_debit_reference',
            'view_field_subscription',
            'view_field_field_1',
            'view_field_field_2',
            'view_field_field_3',
            'view_field_field_4',
            'view_field_field_5'
        ]

        permissionmap = {
            'salutation': {
                'text': 'Salutation',
                'permission': 'view_field_salutation'
            },
            'last_name': {
                'text': 'Lastname',
                'permission': 'view_field_last_name'
            },
            'first_name': {
                'text': 'Firstname',
                'permission': 'view_field_first_name'
            },
            'street': {
                'text': 'Street',
                'permission': 'view_field_street'
            },
            'zipcode': {
                'text': 'Zip-Code',
                'permission': 'view_field_zipcode'
            },
            'city': {
                'text': 'City',
                'permission': 'view_field_city'
            },
            'birthday': {
                'text': 'Birthday',
                'permission': 'view_field_birthday'
            },
            'phone': {
                'text': 'Phone',
                'permission': 'view_field_phone'
            },
            'mobile': {
                'text': 'Mobile',
                'permission': 'view_field_mobile'
            },
            'fax': {
                'text': 'Fax',
                'permission': 'view_field_fax'
            },
            'email': {
                'text': 'EMail',
                'permission': 'view_field_email'
            },
            'membership_number': {
                'text': 'Membership number',
                'permission': 'view_field_membership_number'
            },
            'joined_at': {
                'text': 'Joined at',
                'permission': 'view_field_joined_at'
            },
            'terminated_at': {
                'text': 'Terminated at',
                'permission': 'view_field_terminated_at'
            },
            'division': {
                'text': 'Division',
                'permission': 'view_field_division'
            },
            'payment_method': {
                'text': 'Method',
                'permission': 'view_field_payment_method'
            },
            'iban': {
                'text': 'IBAN',
                'permission': 'view_field_iban'
            },
            'bic': {
                'text': 'BIC',
                'permission': 'view_field_bic'
            },
            'debit_mandate_at': {
                'text': 'Direct debit mandate granted at',
                'permission': 'view_field_debit_mandate_at'
            },
            'debit_reference': {
                'text': 'Direct debit reference',
                'permission': 'view_field_debit_reference'
            },
            'subscription': {
                'text': 'Subscription',
                'permission': 'view_field_subscription'
            },
            'field_1': {
                'text': 'Additional field 1',
                'permission': 'view_field_field_1'
            },
            'field_2': {
                'text': 'Additional field 2',
                'permission': 'view_field_field_2'
            },
            'field_3': {
                'text': 'Additional field 3',
                'permission': 'view_field_field_3'
            },
            'field_4': {
                'text': 'Additional field 4',
                'permission': 'view_field_field_4'
            },
            'field_5': {
                'text': 'Additional field 5',
                'permission': 'view_field_field_5'
            },
        }


        for _, value in permissionmap.items():
            with translation.override('en'):
                response = self.client.get(reverse('members:member_detail', args={Member.objects.get(last_name='Temp').pk}))
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, value['text'])

            for permission in permissions:
                p = Permission.objects.get(codename=permission)
                user.user_permissions.add(p)
                with translation.override('en'):
                    response = self.client.get(reverse('members:member_detail', args={Member.objects.get(last_name='Temp').pk}))
                if permission == value['permission']:
                    self.assertContains(response, value['text'])
                else:
                    self.assertNotContains(response, value['text'])

                user.user_permissions.remove(p)
    
    def test_member_list_division_access_restrictions(self):
        "Member should only be listed if user is not restricted to access the assigned division"
        
        user = User.objects.get(username='temp')    
        user.user_permissions.add(Permission.objects.get(codename='view_member'))
        user.user_permissions.add(Permission.objects.get(codename='view_field_last_name'))
        division = Division.objects.get(name='Temp')
        user2 = User.objects.get(username='temp2')
        group = Group.objects.get(name='group')
        group2 = Group.objects.get(name='group2')

        # Access restrictions for user
        division.user.add(user2)
        response = self.client.get(reverse('members:member_list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Temp')

        division.user.add(user)
        response = self.client.get(reverse('members:member_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Temp')

        division.user.remove(user)
        division.user.remove(user2)

        # Access restrictions for groups
        group.user_set.add(user)
        group2.user_set.add(user2)

        division.groups.add(group2)
        response = self.client.get(reverse('members:member_list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Temp')

        division.groups.add(group)
        response = self.client.get(reverse('members:member_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Temp')

    def test_member_detail_division_access_restrictions(self):
        "Member should only be viewable if user is not restricted to access the assigned division"
        
        user = User.objects.get(username='temp')    
        user.user_permissions.add(Permission.objects.get(codename='view_member'))
        division = Division.objects.get(name='Temp')
        user2 = User.objects.get(username='temp2')
        group = Group.objects.get(name='group')
        group2 = Group.objects.get(name='group2')

        # Access restrictions for user
        division.user.add(user2)
        response = self.client.get(reverse('members:member_detail', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        division.user.add(user)
        response = self.client.get(reverse('members:member_detail', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 200)

        division.user.remove(user)
        division.user.remove(user2)

        # Access restrictions for groups
        group.user_set.add(user)
        group2.user_set.add(user2)

        division.groups.add(group2)
        response = self.client.get(reverse('members:member_detail', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        division.groups.add(group)
        response = self.client.get(reverse('members:member_detail', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_member_edit_division_access_restrictions(self):
        "Member should only be editable if user is not restricted to access the assigned division"
        
        user = User.objects.get(username='temp')    
        user.user_permissions.add(Permission.objects.get(codename='view_member'))
        user.user_permissions.add(Permission.objects.get(codename='change_member'))
        division = Division.objects.get(name='Temp')
        user2 = User.objects.get(username='temp2')
        group = Group.objects.get(name='group')
        group2 = Group.objects.get(name='group2')

        # Access restrictions for user
        division.user.add(user2)
        response = self.client.get(reverse('members:member_edit', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        division.user.add(user)
        response = self.client.get(reverse('members:member_edit', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 200)

        division.user.remove(user)
        division.user.remove(user2)

        # Access restrictions for groups
        group.user_set.add(user)
        group2.user_set.add(user2)

        division.groups.add(group2)
        response = self.client.get(reverse('members:member_edit', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        division.groups.add(group)
        response = self.client.get(reverse('members:member_edit', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 200)

    def test_member_file_upload_permission(self):
        "User should only be able to upload files if permission is set"

        with self.settings(MEDIA_ROOT=self.temp_dir):
            user = User.objects.get(username='temp')
            
            response = self.client.post(reverse('members:member_upload_file', args={Member.objects.get(last_name='Temp').pk}), {'file': SimpleUploadedFile('Testfile.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 403)

            user.user_permissions.add(Permission.objects.get(codename='view_member'))
            response = self.client.post(reverse('members:member_upload_file', args={Member.objects.get(last_name='Temp').pk}), {'file': SimpleUploadedFile('Testfile.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 403)

            user.user_permissions.remove(Permission.objects.get(codename='view_member'))
            user.user_permissions.add(Permission.objects.get(codename='change_member'))
            response = self.client.post(reverse('members:member_upload_file', args={Member.objects.get(last_name='Temp').pk}), {'file': SimpleUploadedFile('Testfile.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 403)

            user.user_permissions.remove(Permission.objects.get(codename='change_member'))
            user.user_permissions.add(Permission.objects.get(codename='view_files'))
            response = self.client.post(reverse('members:member_upload_file', args={Member.objects.get(last_name='Temp').pk}), {'file': SimpleUploadedFile('Testfile.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 403)

            user.user_permissions.add(Permission.objects.get(codename='change_member'))
            response = self.client.post(reverse('members:member_upload_file', args={Member.objects.get(last_name='Temp').pk}), {'file': SimpleUploadedFile('Testfile.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 403)

            user.user_permissions.remove(Permission.objects.get(codename='view_files'))
            user.user_permissions.add(Permission.objects.get(codename='view_member'))
            response = self.client.post(reverse('members:member_upload_file', args={Member.objects.get(last_name='Temp').pk}), {'file': SimpleUploadedFile('Testfile.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 403)

            user.user_permissions.remove(Permission.objects.get(codename='change_member'))
            user.user_permissions.add(Permission.objects.get(codename='view_files'))
            response = self.client.post(reverse('members:member_upload_file', args={Member.objects.get(last_name='Temp').pk}), {'file': SimpleUploadedFile('Testfile.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 403)

            user.user_permissions.add(Permission.objects.get(codename='change_member'))
            response = self.client.post(reverse('members:member_upload_file', args={Member.objects.get(last_name='Temp').pk}), {'file': SimpleUploadedFile('Testfile.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 200)

    def test_member_file_delete_permission(self):
        "User should only be able to delete files if permission is set"

        with self.settings(MEDIA_ROOT=self.temp_dir):
            user = User.objects.get(username='temp')
            user.user_permissions.add(Permission.objects.get(codename='view_member'))
            user.user_permissions.add(Permission.objects.get(codename='change_member'))
            user.user_permissions.add(Permission.objects.get(codename='view_files'))
            self.client.post(reverse('members:member_upload_file', args={Member.objects.get(last_name='Temp').pk}), {'file': SimpleUploadedFile('Testfile.txt', bytes('Test', 'utf-8'))})
            user.user_permissions.remove(Permission.objects.get(codename='view_member'))
            user.user_permissions.remove(Permission.objects.get(codename='change_member'))
            user.user_permissions.remove(Permission.objects.get(codename='view_files'))

                    
            response = self.client.post(reverse('members:member_delete_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 403)

            user.user_permissions.add(Permission.objects.get(codename='view_member'))
            response = self.client.post(reverse('members:member_delete_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 403)

            user.user_permissions.remove(Permission.objects.get(codename='view_member'))
            user.user_permissions.add(Permission.objects.get(codename='change_member'))
            response = self.client.post(reverse('members:member_delete_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 403)

            user.user_permissions.remove(Permission.objects.get(codename='change_member'))
            user.user_permissions.add(Permission.objects.get(codename='view_files'))
            response = self.client.post(reverse('members:member_delete_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 403)

            user.user_permissions.add(Permission.objects.get(codename='change_member'))
            response = self.client.post(reverse('members:member_delete_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 403)

            user.user_permissions.remove(Permission.objects.get(codename='view_files'))
            user.user_permissions.add(Permission.objects.get(codename='view_member'))
            response = self.client.post(reverse('members:member_delete_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 403)

            user.user_permissions.remove(Permission.objects.get(codename='change_member'))
            user.user_permissions.add(Permission.objects.get(codename='view_files'))
            response = self.client.post(reverse('members:member_delete_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 403)

            user.user_permissions.add(Permission.objects.get(codename='change_member'))
            response = self.client.post(reverse('members:member_delete_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 302)
        
    def test_member_file_download_permission(self):
        "User should only be able to download files if permission is set"

        with self.settings(MEDIA_ROOT=self.temp_dir):
            user = User.objects.get(username='temp')
            user.user_permissions.add(Permission.objects.get(codename='view_member'))
            user.user_permissions.add(Permission.objects.get(codename='change_member'))
            user.user_permissions.add(Permission.objects.get(codename='view_files'))
            self.client.post(reverse('members:member_upload_file', args={Member.objects.get(last_name='Temp').pk}), {'file': SimpleUploadedFile('Testfile.txt', bytes('Test', 'utf-8'))})
            user.user_permissions.remove(Permission.objects.get(codename='view_member'))
            user.user_permissions.remove(Permission.objects.get(codename='change_member'))
            user.user_permissions.remove(Permission.objects.get(codename='view_files'))

                    
            response = self.client.get(reverse('members:member_download_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 403)

            user.user_permissions.add(Permission.objects.get(codename='view_member'))
            response = self.client.get(reverse('members:member_download_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 403)

            user.user_permissions.remove(Permission.objects.get(codename='view_member'))
            user.user_permissions.add(Permission.objects.get(codename='view_files'))
            response = self.client.get(reverse('members:member_download_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 403)

            user.user_permissions.add(Permission.objects.get(codename='view_member'))
            response = self.client.get(reverse('members:member_download_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 200)

    def test_member_upload_file_access_restrictions(self):
        "User should only be able to upload files if user is not restricted to access the assigned division"
        
        with self.settings(MEDIA_ROOT=self.temp_dir):
            user = User.objects.get(username='temp')    
            user.user_permissions.add(Permission.objects.get(codename='view_member'))
            user.user_permissions.add(Permission.objects.get(codename='change_member'))
            user.user_permissions.add(Permission.objects.get(codename='view_files'))
            self.client.post(reverse('members:member_upload_file', args={Member.objects.get(last_name='Temp').pk}), {'file': SimpleUploadedFile('Testfile.txt', bytes('Test', 'utf-8'))})
            division = Division.objects.get(name='Temp')
            user2 = User.objects.get(username='temp2')
            group = Group.objects.get(name='group')
            group2 = Group.objects.get(name='group2')

            # Access restrictions for user
            division.user.add(user2)
            response = self.client.post(reverse('members:member_upload_file', args={Member.objects.get(last_name='Temp').pk}), {'file': SimpleUploadedFile('Testfile.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 403)

            division.user.add(user)
            response = self.client.post(reverse('members:member_upload_file', args={Member.objects.get(last_name='Temp').pk}), {'file': SimpleUploadedFile('Testfile.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 200)

            division.user.remove(user)
            division.user.remove(user2)

            # Access restrictions for groups
            group.user_set.add(user)
            group2.user_set.add(user2)

            division.groups.add(group2)
            response = self.client.post(reverse('members:member_upload_file', args={Member.objects.get(last_name='Temp').pk}), {'file': SimpleUploadedFile('Testfile.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 403)

            division.groups.add(group)
            response = self.client.post(reverse('members:member_upload_file', args={Member.objects.get(last_name='Temp').pk}), {'file': SimpleUploadedFile('Testfile.txt', bytes('Test', 'utf-8'))})
            self.assertEqual(response.status_code, 200)
        
    def test_member_download_file_access_restrictions(self):
        "User should only be able to download files if user is not restricted to access the assigned division"
        
        with self.settings(MEDIA_ROOT=self.temp_dir):
            user = User.objects.get(username='temp')    
            user.user_permissions.add(Permission.objects.get(codename='view_member'))
            user.user_permissions.add(Permission.objects.get(codename='change_member'))
            user.user_permissions.add(Permission.objects.get(codename='view_files'))
            self.client.post(reverse('members:member_upload_file', args={Member.objects.get(last_name='Temp').pk}), {'file': SimpleUploadedFile('Testfile.txt', bytes('Test', 'utf-8'))})
            division = Division.objects.get(name='Temp')
            user2 = User.objects.get(username='temp2')
            group = Group.objects.get(name='group')
            group2 = Group.objects.get(name='group2')

            # Access restrictions for user
            division.user.add(user2)
            response = self.client.get(reverse('members:member_download_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 403)

            division.user.add(user)
            response = self.client.get(reverse('members:member_download_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 200)

            division.user.remove(user)
            division.user.remove(user2)

            # Access restrictions for groups
            group.user_set.add(user)
            group2.user_set.add(user2)

            division.groups.add(group2)
            response = self.client.post(reverse('members:member_download_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 403)

            division.groups.add(group)
            response = self.client.post(reverse('members:member_download_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 200)

    def test_member_delete_file_access_restrictions(self):
        "User should only be able to delete files if user is not restricted to access the assigned division"
        
        with self.settings(MEDIA_ROOT=self.temp_dir):
            user = User.objects.get(username='temp')    
            user.user_permissions.add(Permission.objects.get(codename='view_member'))
            user.user_permissions.add(Permission.objects.get(codename='change_member'))
            user.user_permissions.add(Permission.objects.get(codename='view_files'))
            self.client.post(reverse('members:member_upload_file', args={Member.objects.get(last_name='Temp').pk}), {'file': SimpleUploadedFile('Testfile.txt', bytes('Test', 'utf-8'))})
            division = Division.objects.get(name='Temp')
            user2 = User.objects.get(username='temp2')
            group = Group.objects.get(name='group')
            group2 = Group.objects.get(name='group2')

            # Access restrictions for user
            division.user.add(user2)
            response = self.client.post(reverse('members:member_delete_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 403)

            division.user.add(user)
            response = self.client.post(reverse('members:member_delete_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 302)

            division.user.remove(user)
            division.user.remove(user2)

            # Access restrictions for groups
            group.user_set.add(user)
            group2.user_set.add(user2)
            self.client.post(reverse('members:member_upload_file', args={Member.objects.get(last_name='Temp').pk}), {'file': SimpleUploadedFile('Testfile.txt', bytes('Test', 'utf-8'))})
            
            division.groups.add(group2)
            response = self.client.post(reverse('members:member_delete_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 403)

            division.groups.add(group)
            response = self.client.post(reverse('members:member_delete_file', args={File.objects.get(member=Member.objects.get(last_name='Temp')).pk}))
            self.assertEqual(response.status_code, 302)

class DivisionTestMethods(TestCase):
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

        # Create division
        division = Division.objects.create(name='Temp')
        division.save()

    # Test for __str__ method.
    def test__str__(self):
        # Create division.
        division = Division.objects.create(name='Temp')

        # Assert if __str__ ist full name.
        self.assertEqual(str(division), "Temp")

    def test_division_list_permission(self):
        "User should only access division list if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('members:division_list'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_division'))

        response = self.client.get(reverse('members:division_list'))
        self.assertEqual(response.status_code, 200)
  
    def test_division_detail_permission(self):
        "User should only access division detail if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('members:division_detail', args={Division.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_division'))

        response = self.client.get(reverse('members:division_detail', args={Division.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_division_edit_permission(self):
        "User should only access division edit if change permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('members:division_edit', args={Division.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_division'))
        response = self.client.get(reverse('members:division_edit', args={Division.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_division'))
        user.user_permissions.add(Permission.objects.get(codename='change_division'))
        response = self.client.get(reverse('members:division_edit', args={Division.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_division'))
        response = self.client.get(reverse('members:division_edit', args={Division.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_division_create_permission(self):
        "User should only access division create if add permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('members:division_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_division'))
        response = self.client.get(reverse('members:division_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_division'))
        user.user_permissions.add(Permission.objects.get(codename='add_division'))
        response = self.client.get(reverse('members:division_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_division'))
        response = self.client.get(reverse('members:division_create'))
        self.assertEqual(response.status_code, 200)
    
    def test_division_list_access_restrictions(self):
        "Division should only be listed if user is not restricted to access the division"
        
        user = User.objects.get(username='temp')    
        user.user_permissions.add(Permission.objects.get(codename='view_division'))
        division = Division.objects.get(name='Temp')
        user2 = User.objects.get(username='temp2')
        group = Group.objects.get(name='group')
        group2 = Group.objects.get(name='group2')

        # Access restrictions for user
        division.user.add(user2)
        response = self.client.get(reverse('members:division_list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Temp')

        division.user.add(user)
        response = self.client.get(reverse('members:division_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Temp')

        division.user.remove(user)
        division.user.remove(user2)

        # Access restrictions for groups
        group.user_set.add(user)
        group2.user_set.add(user2)

        division.groups.add(group2)
        response = self.client.get(reverse('members:division_list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Temp')

        division.groups.add(group)
        response = self.client.get(reverse('members:division_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Temp')

    def test_division_detail_access_restrictions(self):
        "Division should only be viewable if user is not restricted to access the division"
        
        user = User.objects.get(username='temp')    
        user.user_permissions.add(Permission.objects.get(codename='view_division'))
        division = Division.objects.get(name='Temp')
        user2 = User.objects.get(username='temp2')
        group = Group.objects.get(name='group')
        group2 = Group.objects.get(name='group2')

        # Access restrictions for user
        division.user.add(user2)
        response = self.client.get(reverse('members:division_detail', args={Division.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        division.user.add(user)
        response = self.client.get(reverse('members:division_detail', args={Division.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 200)

        division.user.remove(user)
        division.user.remove(user2)

        # Access restrictions for groups
        group.user_set.add(user)
        group2.user_set.add(user2)

        division.groups.add(group2)
        response = self.client.get(reverse('members:division_detail', args={Division.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        division.groups.add(group)
        response = self.client.get(reverse('members:division_detail', args={Division.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_division_edit_access_restrictions(self):
        "Division should only be editable if user is not restricted to access the division"
        
        user = User.objects.get(username='temp')    
        user.user_permissions.add(Permission.objects.get(codename='view_division'))
        user.user_permissions.add(Permission.objects.get(codename='change_division'))
        division = Division.objects.get(name='Temp')
        user2 = User.objects.get(username='temp2')
        group = Group.objects.get(name='group')
        group2 = Group.objects.get(name='group2')

        # Access restrictions for user
        division.user.add(user2)
        response = self.client.get(reverse('members:division_edit', args={Division.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        division.user.add(user)
        response = self.client.get(reverse('members:division_edit', args={Division.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 200)

        division.user.remove(user)
        division.user.remove(user2)

        # Access restrictions for groups
        group.user_set.add(user)
        group2.user_set.add(user2)

        division.groups.add(group2)
        response = self.client.get(reverse('members:division_edit', args={Division.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        division.groups.add(group)
        response = self.client.get(reverse('members:division_edit', args={Division.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 200)

class SubscriptionTestMethods(TestCase):
    def setUp(self):
        # Create user
        user = User.objects.create_user('temp', 'temp@temp.tld', 'temppass')
        user.first_name = 'temp_first'
        user.last_name = 'temp_last'
        user.save()

        # login with user
        self.client.login(username='temp', password='temppass')

        # Create subscription
        subscription = Subscription.objects.create(name='Temp', amount=123)
        subscription.save()

    # Test for __str__ method.
    def test__str__(self):
        # Create subscription.
        subscription = Subscription.objects.create(name='Temp', amount=123)

        # Assert if __str__ ist full name.
        self.assertEqual(str(subscription), "Temp")

    def test_subscription_list_permission(self):
        "User should only access subscription list if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('members:subscription_list'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_subscription'))

        response = self.client.get(reverse('members:subscription_list'))
        self.assertEqual(response.status_code, 200)
  
    def test_subscription_detail_permission(self):
        "User should only access subscription detail if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('members:subscription_detail', args={Subscription.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_subscription'))

        response = self.client.get(reverse('members:subscription_detail', args={Subscription.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_subscription_edit_permission(self):
        "User should only access subscription edit if change permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('members:subscription_edit', args={Subscription.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_subscription'))
        response = self.client.get(reverse('members:subscription_edit', args={Subscription.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_subscription'))
        user.user_permissions.add(Permission.objects.get(codename='change_subscription'))
        response = self.client.get(reverse('members:subscription_edit', args={Subscription.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_subscription'))
        response = self.client.get(reverse('members:subscription_edit', args={Subscription.objects.get(name='Temp').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_subscription_create_permission(self):
        "User should only access subscription create if add permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('members:subscription_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_subscription'))
        response = self.client.get(reverse('members:subscription_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_subscription'))
        user.user_permissions.add(Permission.objects.get(codename='add_subscription'))
        response = self.client.get(reverse('members:subscription_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_subscription'))
        response = self.client.get(reverse('members:subscription_create'))
        self.assertEqual(response.status_code, 200)