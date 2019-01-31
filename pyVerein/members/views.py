# Import django render shortcut.
from django.shortcuts import render, get_object_or_404 as get
# Import reverse.
from django.urls import reverse, reverse_lazy
# Import members.
from django.views.generic import ListView, DetailView, UpdateView, CreateView
# Import Member.
from .forms import MemberForm, DivisionForm, SubscriptionForm
from .models import Member, Division, Subscription
from finance.models import Transaction
# Import Q for extended filtering.
from django.db.models import Q

# Import localization
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from dynamic_preferences.registries import global_preferences_registry

# Index-View.
class MemberIndexView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'members.view_member'
    template_name = 'members/member/list.html'
    model = Member
    context_object_name = 'members'

# Detail-View.
class MemberDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'members.view_member'
    model = Member
    context_object_name = 'member'
    template_name = 'members/member/detail.html'

# Edit-View.
class MemberEditView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = ('members.view_member', 'members.change_member')
    model = Member
    context_object_name = 'member'
    template_name = 'members/member/edit.html'
    form_class = MemberForm
    success_message = _('Member saved sucessfully')

    def get_success_url(self):
        return reverse_lazy('members:detail', args={self.object.pk})


# Edit-View.
class MemberCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = ('members.view_member', 'members.add_member')
    model = Member
    context_object_name = 'member'
    template_name = 'members/member/create.html'
    form_class = MemberForm
    success_message = _('Member created successfully')

    def get_success_url(self):
        return reverse_lazy('members:detail', args={self.object.pk})

# Index-View.
class DivisionIndexView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'members.view_division'
    template_name = 'members/division/list.html'
    model = Division
    context_object_name = 'divisions'

    def get_context_data(self, **kwargs):
        context = super(DivisionIndexView, self).get_context_data(**kwargs)

        context['divisions'] = []
        for division in Division.objects.all():
            context['divisions'].append({
                'pk': division.pk,
                'name': division.name,
                'members': Member.objects.filter(division=division.pk).count()
            })

        return context
# Detail-View.
class DivisionDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'members.view_division'
    model = Division
    context_object_name = 'division'
    template_name = 'members/division/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DivisionDetailView, self).get_context_data(**kwargs)

        context['members'] = Member.objects.filter(division=self.object.pk)

        return context

# Edit-View.
class DivisionEditView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = ('members.view_division', 'members.change_division')
    model = Division
    context_object_name = 'division'
    template_name = 'members/division/edit.html'
    form_class = DivisionForm
    success_message = _('Division saved succesfully')

    def get_success_url(self):
        return reverse_lazy('members:division_detail', args={self.object.pk})


# Edit-View.
class DivisionCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = ('members.view_division', 'members.add_division')
    model = Division
    context_object_name = 'division'
    template_name = 'members/division/create.html'
    form_class = DivisionForm
    success_message = _('Division created successfully')

    def get_success_url(self):
        return reverse_lazy('members:division_detail', args={self.object.pk})

# Index-View.
class SubscriptionIndexView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'members.view_subscription'
    template_name = 'members/subscription/list.html'
    model = Subscription
    context_object_name = 'subscriptions'

    def get_context_data(self, **kwargs):
        context = super(SubscriptionIndexView, self).get_context_data(**kwargs)

        context['subscriptions'] = []
        for subscription in Subscription.objects.all():
            context['subscriptions'].append({
                'pk': subscription.pk,
                'name': subscription.name,
                'members': Member.objects.filter(subscription=subscription.pk).count()
            })

        return context

# Detail-View.
class SubscriptionDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'members.view_subscription'
    model = Subscription
    context_object_name = 'subscription'
    template_name = 'members/subscription/detail.html'

    def get_context_data(self, **kwargs):
        context = super(SubscriptionDetailView, self).get_context_data(**kwargs)

        context['members'] = Member.objects.filter(subscription=self.object.pk)

        return context

# Edit-View.
class SubscriptionEditView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = ('members.view_subscription', 'members.change_subscription')
    model = Subscription
    context_object_name = 'subscription'
    template_name = 'members/subscription/edit.html'
    form_class = SubscriptionForm
    success_message = _('Subscription saved succesfully')

    def get_success_url(self):
        return reverse_lazy('members:subscription_detail', args={self.object.pk})


# Edit-View.
class SubscriptionCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = ('members.view_subscription', 'members.add_subscription')
    model = Subscription
    context_object_name = 'subscription'
    template_name = 'members/subscription/create.html'
    form_class = SubscriptionForm
    success_message = _('Subscription created successfully')

    def get_success_url(self):
        return reverse_lazy('members:subscription_detail', args={self.object.pk})
