from django.test import TestCase
from account.models import User
from django.urls import reverse
from django.contrib.auth.models import Permission
from datetime import date
from .models import Account, CostObject, CostCenter, Transaction, VirtualAccount
from dynamic_preferences.registries import global_preferences_registry

class AccountTestMethods(TestCase):
    def setUp(self):
        # Create user
        user = User.objects.create_user('temp', 'temp@temp.tld', 'temppass')
        user.first_name = 'temp_first'
        user.last_name = 'temp_last'
        user.save()

        # login with user
        self.client.login(username='temp', password='temppass')

        # Create account
        account = Account.objects.create(number='99999', name='TempAccount', account_type=Account.DEBITOR)
        account.save()

        global_preferences_registry.manager()['Finance__accounting_year'] = str(date.today().year)

    def test_account_search_api_permission(self):
        "User should only access account search api if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:account_search', args={Account.objects.get(number='99999').name}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_account'))

        response = self.client.get(reverse('finance:account_search', args={Account.objects.get(number='99999').name}))
        self.assertEqual(response.status_code, 200)

class DebitorTestMethods(TestCase):
    def setUp(self):
        # Create user
        user = User.objects.create_user('temp', 'temp@temp.tld', 'temppass')
        user.first_name = 'temp_first'
        user.last_name = 'temp_last'
        user.save()

        # login with user
        self.client.login(username='temp', password='temppass')

        # Create debitor
        debitor = Account.objects.create(number='10000', name='TempDebitor', account_type=Account.DEBITOR)
        debitor.save()

        global_preferences_registry.manager()['Finance__accounting_year'] = str(date.today().year)

    def test_debitor_list_permission(self):
        "User should only access debitor list if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:debitor_list'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_debitor'))

        response = self.client.get(reverse('finance:debitor_list'))
        self.assertEqual(response.status_code, 200)
  
    def test_debitor_detail_permission(self):
        "User should only access debitor detail if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:debitor_detail', args={Account.objects.get(number='10000').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_debitor'))

        response = self.client.get(reverse('finance:debitor_detail', args={Account.objects.get(number='10000').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_debitor_edit_permission(self):
        "User should only access debitor edit if view & change permissions are set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:debitor_edit', args={Account.objects.get(number='10000').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_debitor'))
        response = self.client.get(reverse('finance:debitor_edit', args={Account.objects.get(number='10000').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_debitor'))
        user.user_permissions.add(Permission.objects.get(codename='change_debitor'))
        response = self.client.get(reverse('finance:debitor_edit', args={Account.objects.get(number='10000').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_debitor'))
        response = self.client.get(reverse('finance:debitor_edit', args={Account.objects.get(number='10000').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_debitor_create_permission(self):
        "User should only access debitor create if view & add permissions are set"

        user = User.objects.get(username='temp')

        response = self.client.get(reverse('finance:debitor_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_debitor'))
        response = self.client.get(reverse('finance:debitor_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_debitor'))
        user.user_permissions.add(Permission.objects.get(codename='add_debitor'))
        response = self.client.get(reverse('finance:debitor_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_debitor'))
        response = self.client.get(reverse('finance:debitor_create'))
        self.assertEqual(response.status_code, 200)
    
    def test_debitor_clearing_permission(self):
        "User should only access clearing if view & add & change transation permissions are set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:debitor_clear', args={Account.objects.get(number='10000').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        response = self.client.get(reverse('finance:debitor_clear', args={Account.objects.get(number='10000').pk}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='view_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='add_transaction'))
        response = self.client.get(reverse('finance:debitor_clear', args={Account.objects.get(number='10000').pk}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='add_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='change_transaction'))
        response = self.client.get(reverse('finance:debitor_clear', args={Account.objects.get(number='10000').pk}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='change_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='add_transaction'))
        response = self.client.get(reverse('finance:debitor_clear', args={Account.objects.get(number='10000').pk}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.remove(Permission.objects.get(codename='add_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='change_transaction'))
        response = self.client.get(reverse('finance:debitor_clear', args={Account.objects.get(number='10000').pk}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.remove(Permission.objects.get(codename='change_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='add_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='change_transaction'))
        response = self.client.get(reverse('finance:debitor_clear', args={Account.objects.get(number='10000').pk}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='add_transaction'))
        user.user_permissions.remove(Permission.objects.get(codename='change_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='add_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='change_transaction'))
        response = self.client.get(reverse('finance:debitor_clear', args={Account.objects.get(number='10000').pk}))
        self.assertEqual(response.status_code, 200)

class CreditorTestMethods(TestCase):
    def setUp(self):
        # Create user
        user = User.objects.create_user('temp', 'temp@temp.tld', 'temppass')
        user.first_name = 'temp_first'
        user.last_name = 'temp_last'
        user.save()

        # login with user
        self.client.login(username='temp', password='temppass')

        # Create creditor
        creditor = Account.objects.create(number='70000', name='TempCreditor', account_type=Account.CREDITOR)
        creditor.save()

        global_preferences_registry.manager()['Finance__accounting_year'] = str(date.today().year)

    def test_creditor_list_permission(self):
        "User should only access creditor list if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:creditor_list'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_creditor'))

        response = self.client.get(reverse('finance:creditor_list'))
        self.assertEqual(response.status_code, 200)
  
    def test_creditor_detail_permission(self):
        "User should only access creditor detail if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:creditor_detail', args={Account.objects.get(number='70000').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_creditor'))

        response = self.client.get(reverse('finance:creditor_detail', args={Account.objects.get(number='70000').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_creditor_edit_permission(self):
        "User should only access creditor edit if view & change permissions are set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:creditor_edit', args={Account.objects.get(number='70000').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_creditor'))
        response = self.client.get(reverse('finance:creditor_edit', args={Account.objects.get(number='70000').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_creditor'))
        user.user_permissions.add(Permission.objects.get(codename='change_creditor'))
        response = self.client.get(reverse('finance:creditor_edit', args={Account.objects.get(number='70000').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_creditor'))
        response = self.client.get(reverse('finance:creditor_edit', args={Account.objects.get(number='70000').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_creditor_create_permission(self):
        "User should only access creditor create if view & add permissions are set"

        user = User.objects.get(username='temp')

        response = self.client.get(reverse('finance:creditor_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_creditor'))
        response = self.client.get(reverse('finance:creditor_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_creditor'))
        user.user_permissions.add(Permission.objects.get(codename='add_creditor'))
        response = self.client.get(reverse('finance:creditor_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_creditor'))
        response = self.client.get(reverse('finance:creditor_create'))
        self.assertEqual(response.status_code, 200)
        
    def test_creditor_clearing_perm7ssion(self):
        "User should only access clearing if view & add & change transation permissions are set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:creditor_clear', args={Account.objects.get(number='70000').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        response = self.client.get(reverse('finance:creditor_clear', args={Account.objects.get(number='70000').pk}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='view_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='add_transaction'))
        response = self.client.get(reverse('finance:creditor_clear', args={Account.objects.get(number='70000').pk}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='add_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='change_transaction'))
        response = self.client.get(reverse('finance:creditor_clear', args={Account.objects.get(number='70000').pk}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='change_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='add_transaction'))
        response = self.client.get(reverse('finance:creditor_clear', args={Account.objects.get(number='70000').pk}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.remove(Permission.objects.get(codename='add_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='change_transaction'))
        response = self.client.get(reverse('finance:creditor_clear', args={Account.objects.get(number='70000').pk}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.remove(Permission.objects.get(codename='change_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='add_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='change_transaction'))
        response = self.client.get(reverse('finance:creditor_clear', args={Account.objects.get(number='70000').pk}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='add_transaction'))
        user.user_permissions.remove(Permission.objects.get(codename='change_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='add_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='change_transaction'))
        response = self.client.get(reverse('finance:creditor_clear', args={Account.objects.get(number='70000').pk}))
        self.assertEqual(response.status_code, 200)

class ImpersonalTestMethods(TestCase):
    def setUp(self):
        # Create user
        user = User.objects.create_user('temp', 'temp@temp.tld', 'temppass')
        user.first_name = 'temp_first'
        user.last_name = 'temp_last'
        user.save()

        # login with user
        self.client.login(username='temp', password='temppass')

        # Create impersonal
        impersonal = Account.objects.create(number='4000', name='TempImpersonal', account_type=Account.INCOME)
        impersonal.save()

        global_preferences_registry.manager()['Finance__accounting_year'] = str(date.today().year)

    def test_impersonal_list_permission(self):
        "User should only access impersonal list if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:impersonal_list'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_impersonal'))

        response = self.client.get(reverse('finance:impersonal_list'))
        self.assertEqual(response.status_code, 200)
  
    def test_impersonal_detail_permission(self):
        "User should only access impersonal detail if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:impersonal_detail', args={Account.objects.get(number='4000').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_impersonal'))

        response = self.client.get(reverse('finance:impersonal_detail', args={Account.objects.get(number='4000').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_impersonal_edit_permission(self):
        "User should only access impersonal edit if view & change permissions are set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:impersonal_edit', args={Account.objects.get(number='4000').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_impersonal'))
        response = self.client.get(reverse('finance:impersonal_edit', args={Account.objects.get(number='4000').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_impersonal'))
        user.user_permissions.add(Permission.objects.get(codename='change_impersonal'))
        response = self.client.get(reverse('finance:impersonal_edit', args={Account.objects.get(number='4000').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_impersonal'))
        response = self.client.get(reverse('finance:impersonal_edit', args={Account.objects.get(number='4000').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_impersonal_create_permission(self):
        "User should only access impersonal create if view & add permissions are set"

        user = User.objects.get(username='temp')

        response = self.client.get(reverse('finance:impersonal_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_impersonal'))
        response = self.client.get(reverse('finance:impersonal_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_impersonal'))
        user.user_permissions.add(Permission.objects.get(codename='add_impersonal'))
        response = self.client.get(reverse('finance:impersonal_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_impersonal'))
        response = self.client.get(reverse('finance:impersonal_create'))
        self.assertEqual(response.status_code, 200)

class CostCenterTestMethods(TestCase):
    def setUp(self):
        # Create user
        user = User.objects.create_user('temp', 'temp@temp.tld', 'temppass')
        user.first_name = 'temp_first'
        user.last_name = 'temp_last'
        user.save()

        # login with user
        self.client.login(username='temp', password='temppass')

        # Create costcenter
        costcenter = CostCenter.objects.create(number='101', name='TempCostCenter')
        costcenter.save()

        global_preferences_registry.manager()['Finance__accounting_year'] = str(date.today().year)

    def test_costcenter_list_permission(self):
        "User should only access costcenter list if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:costcenter_list'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_costcenter'))

        response = self.client.get(reverse('finance:costcenter_list'))
        self.assertEqual(response.status_code, 200)
  
    def test_costcenter_detail_permission(self):
        "User should only access costcenter detail if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:costcenter_detail', args={CostCenter.objects.get(number='101').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_costcenter'))

        response = self.client.get(reverse('finance:costcenter_detail', args={CostCenter.objects.get(number='101').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_costcenter_edit_permission(self):
        "User should only access costcenter edit if view & change permissions are set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:costcenter_edit', args={CostCenter.objects.get(number='101').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_costcenter'))
        response = self.client.get(reverse('finance:costcenter_edit', args={CostCenter.objects.get(number='101').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_costcenter'))
        user.user_permissions.add(Permission.objects.get(codename='change_costcenter'))
        response = self.client.get(reverse('finance:costcenter_edit', args={CostCenter.objects.get(number='101').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_costcenter'))
        response = self.client.get(reverse('finance:costcenter_edit', args={CostCenter.objects.get(number='101').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_costcenter_create_permission(self):
        "User should only access costcenter create if view & add permissions are set"

        user = User.objects.get(username='temp')

        response = self.client.get(reverse('finance:costcenter_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_costcenter'))
        response = self.client.get(reverse('finance:costcenter_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_costcenter'))
        user.user_permissions.add(Permission.objects.get(codename='add_costcenter'))
        response = self.client.get(reverse('finance:costcenter_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_costcenter'))
        response = self.client.get(reverse('finance:costcenter_create'))
        self.assertEqual(response.status_code, 200)

    def test_costcenter_search_api_permission(self):
        "User should only access costcenter search api if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:costcenter_search', args={CostCenter.objects.get(number='101').name}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_costcenter'))

        response = self.client.get(reverse('finance:costcenter_search', args={CostCenter.objects.get(number='101').name}))
        self.assertEqual(response.status_code, 200)

class CostObjectTestMethods(TestCase):
    def setUp(self):
        # Create user
        user = User.objects.create_user('temp', 'temp@temp.tld', 'temppass')
        user.first_name = 'temp_first'
        user.last_name = 'temp_last'
        user.save()

        # login with user
        self.client.login(username='temp', password='temppass')

        # Create costobject
        costobject = CostObject.objects.create(number='101', name='TempCostObject')
        costobject.save()

        global_preferences_registry.manager()['Finance__accounting_year'] = str(date.today().year)


    def test_costobject_list_permission(self):
        "User should only access costobject list if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:costobject_list'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_costobject'))

        response = self.client.get(reverse('finance:costobject_list'))
        self.assertEqual(response.status_code, 200)
  
    def test_costobject_detail_permission(self):
        "User should only access costobject detail if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:costobject_detail', args={CostObject.objects.get(number='101').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_costobject'))

        response = self.client.get(reverse('finance:costobject_detail', args={CostObject.objects.get(number='101').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_costobject_edit_permission(self):
        "User should only access costobject edit if view & change permissions are set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:costobject_edit', args={CostObject.objects.get(number='101').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_costobject'))
        response = self.client.get(reverse('finance:costobject_edit', args={CostObject.objects.get(number='101').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_costobject'))
        user.user_permissions.add(Permission.objects.get(codename='change_costobject'))
        response = self.client.get(reverse('finance:costobject_edit', args={CostObject.objects.get(number='101').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_costobject'))
        response = self.client.get(reverse('finance:costobject_edit', args={CostObject.objects.get(number='101').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_costobject_create_permission(self):
        "User should only access costobject create if view & add permissions are set"

        user = User.objects.get(username='temp')

        response = self.client.get(reverse('finance:costobject_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_costobject'))
        response = self.client.get(reverse('finance:costobject_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_costobject'))
        user.user_permissions.add(Permission.objects.get(codename='add_costobject'))
        response = self.client.get(reverse('finance:costobject_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_costobject'))
        response = self.client.get(reverse('finance:costobject_create'))
        self.assertEqual(response.status_code, 200)

    def test_costobject_search_api_permission(self):
        "User should only access costobject search api if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:costobject_search', args={CostObject.objects.get(number='101').name}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_costobject'))

        response = self.client.get(reverse('finance:costobject_search', args={CostObject.objects.get(number='101').name}))
        self.assertEqual(response.status_code, 200)

class TransactionTestMethods(TestCase):
    def setUp(self):
        # Create user
        user = User.objects.create_user('temp', 'temp@temp.tld', 'temppass')
        user.first_name = 'temp_first'
        user.last_name = 'temp_last'
        user.save()

        # login with user
        self.client.login(username='temp', password='temppass')

        # Create debitor
        debitor = Account.objects.create(number='10000', name='TempDebitor', account_type=Account.DEBITOR)
        debitor.save()
        # Create transaction
        transaction = Transaction.objects.create(account=debitor, date=date.today(), document_number='12345', text='document', debit=123.45, internal_number=1)
        transaction.save()

        global_preferences_registry.manager()['Finance__accounting_year'] = str(date.today().year)

    def test_transaction_list_permission(self):
        "User should only access transaction list if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:transaction_list'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))

        response = self.client.get(reverse('finance:transaction_list'))
        self.assertEqual(response.status_code, 200)
  
    def test_transaction_detail_permission(self):
        "User should only access transaction detail if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:transaction_detail', kwargs={'internal_number': Transaction.objects.get(document_number='12345').internal_number}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))

        response = self.client.get(reverse('finance:transaction_detail', kwargs={'internal_number': Transaction.objects.get(document_number='12345').internal_number}))
        self.assertEqual(response.status_code, 200)
    
    def test_transaction_edit_permission(self):
        "User should only access transaction edit if view & change permissions are set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:transaction_edit', kwargs={'internal_number': Transaction.objects.get(document_number='12345').internal_number, 'pk': Transaction.objects.get(document_number='12345').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        response = self.client.get(reverse('finance:transaction_edit', kwargs={'internal_number': Transaction.objects.get(document_number='12345').internal_number, 'pk': Transaction.objects.get(document_number='12345').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='change_transaction'))
        response = self.client.get(reverse('finance:transaction_edit', kwargs={'internal_number': Transaction.objects.get(document_number='12345').internal_number, 'pk': Transaction.objects.get(document_number='12345').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        response = self.client.get(reverse('finance:transaction_edit', kwargs={'internal_number': Transaction.objects.get(document_number='12345').internal_number, 'pk': Transaction.objects.get(document_number='12345').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_transaction_create_permission(self):
        "User should only access transaction create if view & add permissions are set"

        user = User.objects.get(username='temp')

        response = self.client.get(reverse('finance:transaction_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        response = self.client.get(reverse('finance:transaction_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='add_transaction'))
        response = self.client.get(reverse('finance:transaction_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        response = self.client.get(reverse('finance:transaction_create'))
        self.assertEqual(response.status_code, 200)

    def test_transaction_reset_permission(self):
        "User should only access reset transaction if view & add & change permissions are set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:transaction_reset', args={Transaction.objects.get(document_number='12345').internal_number}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        response = self.client.get(reverse('finance:transaction_reset', args={Transaction.objects.get(document_number='12345').internal_number}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='view_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='add_transaction'))
        response = self.client.get(reverse('finance:transaction_reset', args={Transaction.objects.get(document_number='12345').internal_number}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='add_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='change_transaction'))
        response = self.client.get(reverse('finance:transaction_reset', args={Transaction.objects.get(document_number='12345').internal_number}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='change_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='add_transaction'))
        response = self.client.get(reverse('finance:transaction_reset', args={Transaction.objects.get(document_number='12345').internal_number}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.remove(Permission.objects.get(codename='add_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='change_transaction'))
        response = self.client.get(reverse('finance:transaction_reset', args={Transaction.objects.get(document_number='12345').internal_number}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.remove(Permission.objects.get(codename='change_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='add_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='change_transaction'))
        response = self.client.get(reverse('finance:transaction_reset', args={Transaction.objects.get(document_number='12345').internal_number}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='add_transaction'))
        user.user_permissions.remove(Permission.objects.get(codename='change_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='add_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='change_transaction'))
        response = self.client.get(reverse('finance:transaction_reset', args={Transaction.objects.get(document_number='12345').internal_number}))
        self.assertEqual(response.status_code, 302)
    
    def test_transaction_reset_new_permission(self):
        "User should only access reset & new transaction if view & add & change permissions are set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:transaction_reset_new', args={Transaction.objects.get(document_number='12345').internal_number}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        response = self.client.get(reverse('finance:transaction_reset_new', args={Transaction.objects.get(document_number='12345').internal_number}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='view_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='add_transaction'))
        response = self.client.get(reverse('finance:transaction_reset_new', args={Transaction.objects.get(document_number='12345').internal_number}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='add_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='change_transaction'))
        response = self.client.get(reverse('finance:transaction_reset_new', args={Transaction.objects.get(document_number='12345').internal_number}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='change_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='add_transaction'))
        response = self.client.get(reverse('finance:transaction_reset_new', args={Transaction.objects.get(document_number='12345').internal_number}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.remove(Permission.objects.get(codename='add_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='change_transaction'))
        response = self.client.get(reverse('finance:transaction_reset_new', args={Transaction.objects.get(document_number='12345').internal_number}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.remove(Permission.objects.get(codename='change_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='add_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='change_transaction'))
        response = self.client.get(reverse('finance:transaction_reset_new', args={Transaction.objects.get(document_number='12345').internal_number}))
        self.assertEqual(response.status_code, 403)
        user.user_permissions.remove(Permission.objects.get(codename='add_transaction'))
        user.user_permissions.remove(Permission.objects.get(codename='change_transaction'))

        user.user_permissions.add(Permission.objects.get(codename='view_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='add_transaction'))
        user.user_permissions.add(Permission.objects.get(codename='change_transaction'))
        response = self.client.get(reverse('finance:transaction_reset_new', args={Transaction.objects.get(document_number='12345').internal_number}))
        self.assertEqual(response.status_code, 302)

class VirtualAccountTestMethods(TestCase):
    def setUp(self):
        # Create user
        user = User.objects.create_user('temp', 'temp@temp.tld', 'temppass')
        user.first_name = 'temp_first'
        user.last_name = 'temp_last'
        user.save()

        # login with user
        self.client.login(username='temp', password='temppass')

        # Create virtualaccount
        virtualaccount = VirtualAccount.objects.create(number='101', name='TempVirtualAccount', initial=1000, active_from=date.today())
        virtualaccount.save()

        global_preferences_registry.manager()['Finance__accounting_year'] = str(date.today().year)


    def test_virtualaccount_list_permission(self):
        "User should only access virtualaccount list if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:virtual_account_list'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_virtualaccount'))

        response = self.client.get(reverse('finance:virtual_account_list'))
        self.assertEqual(response.status_code, 200)
  
    def test_virtualaccount_detail_permission(self):
        "User should only access virtualaccount detail if view permission is set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:virtual_account_detail', args={VirtualAccount.objects.get(number='101').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_virtualaccount'))

        response = self.client.get(reverse('finance:virtual_account_detail', args={VirtualAccount.objects.get(number='101').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_virtualaccount_edit_permission(self):
        "User should only access virtualaccount edit if view & change permissions are set"

        user = User.objects.get(username='temp')
        
        response = self.client.get(reverse('finance:virtual_account_edit', args={VirtualAccount.objects.get(number='101').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_virtualaccount'))
        response = self.client.get(reverse('finance:virtual_account_edit', args={VirtualAccount.objects.get(number='101').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_virtualaccount'))
        user.user_permissions.add(Permission.objects.get(codename='change_virtualaccount'))
        response = self.client.get(reverse('finance:virtual_account_edit', args={VirtualAccount.objects.get(number='101').pk}))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_virtualaccount'))
        response = self.client.get(reverse('finance:virtual_account_edit', args={VirtualAccount.objects.get(number='101').pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_virtualaccount_create_permission(self):
        "User should only access virtualaccount create if view & add permissions are set"

        user = User.objects.get(username='temp')

        response = self.client.get(reverse('finance:virtual_account_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_virtualaccount'))
        response = self.client.get(reverse('finance:virtual_account_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.remove(Permission.objects.get(codename='view_virtualaccount'))
        user.user_permissions.add(Permission.objects.get(codename='add_virtualaccount'))
        response = self.client.get(reverse('finance:virtual_account_create'))
        self.assertEqual(response.status_code, 403)

        user.user_permissions.add(Permission.objects.get(codename='view_virtualaccount'))
        response = self.client.get(reverse('finance:virtual_account_create'))
        self.assertEqual(response.status_code, 200)