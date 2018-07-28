from django.views.generic import DetailView, UpdateView
# Import reverse.
from django.urls import reverse_lazy
# Import User/UserProfile.
from .forms import UserForm
from .models import User

from django.contrib.auth.mixins import LoginRequiredMixin

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
