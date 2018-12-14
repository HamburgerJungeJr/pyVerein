from dynamic_preferences.types import BooleanPreference, IntegerPreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry


# Define preferences section for members.
members = Section('Members')

# Register switch for additional field 1
@global_preferences_registry.register
class ShowAdditionalField1(BooleanPreference):
    section = members
    name = 'show_additional_field_1'
    default = False
    verbose_name = "Show additional field 1"

# Register switch for additional field 2
@global_preferences_registry.register
class ShowAdditionalField2(BooleanPreference):
    section = members
    name = 'show_additional_field_2'
    default = False
    verbose_name = "Show additional field 2"
    
# Register switch for additional field 3
@global_preferences_registry.register
class ShowAdditionalField3(BooleanPreference):
    section = members
    name = 'show_additional_field_3'
    default = False
    verbose_name = "Show additional field 3"

# Register switch for additional field 4
@global_preferences_registry.register
class ShowAdditionalField4(BooleanPreference):
    section = members
    name = 'show_additional_field_4'
    default = False
    verbose_name = "Show additional field 4"

# Register switch for additional field 5
@global_preferences_registry.register
class ShowAdditionalField5(BooleanPreference):
    section = members
    name = 'show_additional_field_5'
    default = False
    verbose_name = "Show additional field 5"

# Register input for keeping terminated members timespan
@global_preferences_registry.register
class KeepMembers(IntegerPreference):
    section = members
    name = 'keep_terminated_members'
    default = 365
    verbose_name = "Keep terminated members for days after termination"