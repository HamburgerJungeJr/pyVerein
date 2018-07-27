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
