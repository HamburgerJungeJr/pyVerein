# Import reverse.
from django.urls import reverse_lazy
# Import members.
from django.views.generic import ListView, UpdateView, CreateView, TemplateView
# Import Member.
from .forms import MemberForm, DivisionForm, SubscriptionForm
from .models import Member, Division, Subscription, File

# Import localization
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.db import Error, connection
import os
from django.conf import settings
from sendfile import sendfile
from utils.views import DetailView

# Index-View.
class MemberIndexView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'members.view_member'
    template_name = 'members/member/list.html'

    def get_context_data(self, **kwargs):
        context = super(MemberIndexView, self).get_context_data(**kwargs)

        members = []
        for member in Member.objects.all():
            if member.division.all():
               for division in member.division.all():
                    if division.is_access_granted(self.request.user):
                        members.append(member)
                        break
            else:
                members.append(member)

        context['members'] = members

        return context

# Detail-View.
class MemberDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'members.view_member'
    model = Member
    context_object_name = 'member'
    template_name = 'members/member/detail.html'

    def get_context_data(self, **kwargs):
        context = super(MemberDetailView, self).get_context_data(**kwargs)

        context['files'] = File.objects.filter(member=self.object)

        return context

    def has_permission(self):
        super_perm = super(MemberDetailView, self).has_permission()

        member = Member.objects.get(pk=self.kwargs['pk'])
        if member.division.all():
            for division in member.division.all():
                if division.is_access_granted(self.request.user):
                    return super_perm
            return False
        return super_perm

# Edit-View.
class MemberEditView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = ('members.view_member', 'members.change_member')
    model = Member
    context_object_name = 'member'
    template_name = 'members/member/edit.html'
    form_class = MemberForm
    success_message = _('Member saved sucessfully')

    def get_success_url(self):
        return reverse_lazy('members:member_detail', args={self.object.pk})
    
    def has_permission(self):
        super_perm = super(MemberEditView, self).has_permission()

        member = Member.objects.get(pk=self.kwargs['pk'])
        if member.division.all():
            for division in member.division.all():
                if division.is_access_granted(self.request.user):
                    return super_perm 
            return False
        return super_perm

    def form_valid(self, form):
        # Save validated data
        self.object = form.save(commit = False)

        # Update subscription list for history
        
        self.object.subscriptions = ",".join([s.name for s in Subscription.objects.filter(pk__in=self.request.POST.getlist('subscription'))])
        self.object.devisions = ",".join([s.name for s in Division.objects.filter(pk__in=self.request.POST.getlist('division'))])
        
        return super().form_valid(form)


# Create-View.
class MemberCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = ('members.view_member', 'members.add_member')
    model = Member
    context_object_name = 'member'
    template_name = 'members/member/create.html'
    form_class = MemberForm
    success_message = _('Member created successfully')

    def get_success_url(self):
        return reverse_lazy('members:member_detail', args={self.object.pk})

@login_required
@permission_required(['members.view_member', 'members.change_member', 'members.view_files'], raise_exception=True)
def upload_file(request, pk):
    """
    Upload for member files
    """
    if request.method == 'POST':
        member = Member.objects.get(pk=pk)

        # Check if user can access member
        if member.division.all():
            access = False
            for division in member.division.all():
                if division.is_access_granted(request.user):
                    access = True
                    break
            if not access:        
                return HttpResponseForbidden()

        try:
            file = File(member=member, file=request.FILES['file'])
            file.save()

            # Update file list for history
            member.files = ",".join([os.path.basename(f.file.file.name) for f in File.objects.filter(member=member)])
            member.save()
        except Error as err:
            return JsonResponse({'error': err})

        return JsonResponse({'state': 'success'})
    else:
        return HttpResponseBadRequest()    

@login_required
@permission_required(['members.view_member', 'members.change_member', 'members.view_files'], raise_exception=True)
def delete_file(request, pk):
    """
    Delete member files
    """
    if request.method == 'POST':
        file = File.objects.get(pk=pk)
        member = file.member

        # Check if user can access member
        if member.division.all():
            access = False
            for division in member.division.all():
                if division.is_access_granted(request.user):
                    access = True
                    break
            if not access:        
                return HttpResponseForbidden()

        file.delete()
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, file.file.path)):
            os.remove(os.path.join(settings.MEDIA_ROOT, file.file.path))

        # Update file list for history
        member.files = ",".join([os.path.basename(f.file.file.name) for f in File.objects.filter(member=member)])
        member.save()
        return HttpResponseRedirect(reverse_lazy('members:member_detail', kwargs={'pk': member.pk}))
    else:
        return HttpResponseBadRequest() 
        
@login_required
@permission_required(['members.view_member', 'members.view_files'], raise_exception=True)
def download_file(request, pk):
    """
    Download file with X-SENDFILE header
    """
    file = File.objects.get(pk=pk)
    # Check if user can access member
    if file.member.division.all():
        access = False
        for division in file.member.division.all():
            if division.is_access_granted(request.user):
                access = True
                break
        if not access:        
            return HttpResponseForbidden()


    file = file.file
    return sendfile(request, file.path, attachment=True, attachment_filename=os.path.basename(file.name))

# Index-View.
class DivisionIndexView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'members.view_division'
    template_name = 'members/division/list.html'
    model = Division
    context_object_name = 'divisions'

    def get_context_data(self, **kwargs):
        context = super(DivisionIndexView, self).get_context_data(**kwargs)

        context['divisions'] = []
        divisions = [division for division in Division.objects.all() if division.is_access_granted(self.request.user)]
        for division in divisions:
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
    
    def has_permission(self):
        super_perm = super(DivisionDetailView, self).has_permission()
        return super_perm and Division.objects.get(pk=self.kwargs['pk']).is_access_granted(self.request.user)

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

    def has_permission(self):
        super_perm = super(DivisionEditView, self).has_permission()
        return super_perm and Division.objects.get(pk=self.kwargs['pk']).is_access_granted(self.request.user)

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

        members = []
        for member in Member.objects.filter(subscription=self.object.pk):
            if member.division.all():
               for division in member.division.all():
                    if division.is_access_granted(self.request.user):
                        members.append(member)
                        break
            else:
                members.append(member)
                
        context['members'] = members
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
