from django.test import TestCase
from .models import Member
from datetime import datetime, timedelta
from account.models import User
from django.urls import reverse
from django.contrib.auth.models import Permission

class MemberTestMethods(TestCase):
    def setUp(self):
        # Create user
        user = User.objects.create_user('temp', 'temp@temp.tld', 'temppass')
        user.first_name = 'temp_first'
        user.last_name = 'temp_last'
        user.save()

        # login with user
        self.client.login(username='temp', password='temppass')

        # Create member
        member = Member.objects.create(salutation=Member.MR, first_name='Temp', last_name='Temp')
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
        
        response = self.client.get(reverse('members:list'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_member'))

        response = self.client.get(reverse('members:list'))
        self.assertEqual(response.status_code, 200)
  
    def test_member_detail_permission(self):
        "User should only access member detail if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('members:detail', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_member'))

        response = self.client.get(reverse('members:detail', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_member_edit_permission(self):
        "User should only access member edit if change permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('members:edit', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='change_member'))

        response = self.client.get(reverse('members:edit', args={Member.objects.get(last_name='Temp').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_member_create_permission(self):
        "User should only access member create if add permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('members:create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='add_member'))

        response = self.client.get(reverse('members:create'))
        self.assertEqual(response.status_code, 200)
    
    def test_member_list_permission(self):
        "User should only access member api if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('members:apiList'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_member'))

        response = self.client.get(reverse('members:apiList'))
        self.assertEqual(response.status_code, 200)