from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User

class AccountCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('avatar', )

class AccountChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('avatar', )

class AccountAdmin(UserAdmin):
    add_form = AccountCreationForm
    form = AccountChangeForm

admin.site.register(User, AccountAdmin)
