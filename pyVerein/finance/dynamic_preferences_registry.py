from dynamic_preferences.types import StringPreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry


# Define preferences section for finance.
finance = Section('Finance')

# Register input for Reset prefix
@global_preferences_registry.register
class ResetPrefix(StringPreference):
    section = finance
    name = 'reset_prefix'
    default = ''
    verbose_name = "Documentnumber prefix for reset receipts"

# Register input for currency
@global_preferences_registry.register
class Currency(StringPreference):
    section = finance
    name = 'currency'
    default = '€'
    verbose_name = "Currency sign"

# Register input for currency
@global_preferences_registry.register
class AccountingYear(StringPreference):
    section = finance
    name = 'accounting_year'
    default = ''
    verbose_name = "Acounting year"