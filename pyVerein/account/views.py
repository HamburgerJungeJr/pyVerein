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

class UserDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view for User
    """
    model = User
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

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