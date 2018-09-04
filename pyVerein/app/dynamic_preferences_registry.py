from dynamic_preferences.types import StringPreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from finance.models import Account

# Define preferences section for dashboard.
dashboard = Section('Dashboard')

# Register input for dashboard bank accounts
@global_preferences_registry.register
class BankAccount(StringPreference):
    section = dashboard
    name = 'bank_accounts'
    default = ''
    verbose_name = "Bank accounts to show on dashboard chart"