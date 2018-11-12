from dynamic_preferences.types import StringPreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry


# Define preferences section for tasks.
tasks = Section('Tasks')

# Register input for subscription income account
@global_preferences_registry.register
class SubscriptionIncomeAccount(StringPreference):
    section = tasks
    name = 'subscription_income_account'
    default = ''
    verbose_name = "Incomeaccount for subscriptions of members"

# Register input for subscription debitor account
@global_preferences_registry.register
class SubscriptionDebitorAccount(StringPreference):
    section = tasks
    name = 'subscription_debitor_account'
    default = ''
    verbose_name = "Debitoraccount for subscriptions of members"

# Register input for subscription cost center
@global_preferences_registry.register
class SubscriptionCostCenter(StringPreference):
    section = tasks
    name = 'subscription_cost_center'
    default = ''
    verbose_name = "Cost center for subscriptions of members"


# Register input for subscription cost object
@global_preferences_registry.register
class SubscriptionCostObject(StringPreference):
    section = tasks
    name = 'subscription_cost_object'
    default = ''
    verbose_name = "Cost object for subscriptions of members"