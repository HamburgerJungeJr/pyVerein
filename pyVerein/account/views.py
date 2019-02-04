from django.views.generic import DetailView, UpdateView
# Import reverse.
from django.urls import reverse_lazy
# Import User/UserProfile.
from .forms import UserForm
from .models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from two_factor.utils import default_device
from django_otp.plugins.otp_static.models import StaticDevice
from two_factor import views

class UserDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view for User
    """
    model = User
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        try:
            backup_device = self.request.user.staticdevice_set.get(name='backup')
        except StaticDevice.DoesNotExist:
            backup_device = None

        return {
            'default_device': default_device(self.request.user),
            'default_device_type': default_device(self.request.user).__class__.__name__,
            'backup_device': backup_device,
        }

class UserEditView(LoginRequiredMixin, UpdateView):
    """
    Edit view for User.
    """
    model = User
    context_object_name = 'user'
    template_name = 'account/user_edit.html'
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('account:detail')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('account:detail')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {
        'form': form
    })

class BackupTokensView(views.BackupTokensView):
    success_url = 'account:detail'

class SetupView(views.SetupView):
    success_url = 'account:two_factor_setup_complete'
    qrcode_url = 'account:two_factor_qr'