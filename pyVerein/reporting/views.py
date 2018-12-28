# Import reverse.
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
from django.db import Error
# Import Report.
from .forms import ReportForm, ResourceForm
from .models import Report, Resource
import os
from django.conf import settings

# Import localization
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from sendfile import sendfile

# Index-View.
class ReportIndexView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'reporting.view_report'
    model = Report
    context_object_name = 'reports'
    template_name = 'reporting/list.html'

# Detail-View.
class ReportDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'reporting.view_report'
    model = Report
    context_object_name = 'report'
    template_name = 'reporting/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ReportDetailView, self).get_context_data(**kwargs)

        context['resources'] = Resource.objects.filter(report=self.object)

        return context

# Edit-View.
class ReportEditView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = ('reporting.view_report', 'reporting.change_report')
    model = Report
    context_object_name = 'report'
    template_name = 'reporting/edit.html'
    form_class = ReportForm
    success_message = _('Report saved sucessfully')

    def get_success_url(self):
        return reverse_lazy('reporting:detail', args={self.object.pk})

# Edit-View.
class ReportCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = ('reporting.view_report', 'reporting.add_report')
    model = Report
    context_object_name = 'report'
    template_name = 'reporting/create.html'
    form_class = ReportForm
    success_message = _('Report created successfully')

    def get_success_url(self):
        return reverse_lazy('reporting:detail', args={self.object.pk})

@login_required
@permission_required(['reporting.view_report', 'reporting.change_report'], raise_exception=True)
def upload_resource(request, pk):
    """
    Upload for report resources
    """
    if request.method == 'POST':
        try:
            resource = Resource(report=Report.objects.get(pk=pk), resource=request.FILES['resource'])
            resource.save()
        except Error as err:
            return JsonResponse({'error': err})
        
        return JsonResponse({'state': 'success'})
    else:
        return HttpResponseBadRequest()    

@login_required
@permission_required(['reporting.view_report', 'reporting.change_report'], raise_exception=True)
def delete_resource(request, pk):
    """
    Delete report resources
    """
    if request.method == 'POST':
        resource = Resource.objects.get(pk=pk)
        report = resource.report
        resource.delete()
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, resource.resource.path)):
            os.remove(os.path.join(settings.MEDIA_ROOT, resource.resource.path))
        return HttpResponseRedirect(reverse_lazy('reporting:detail', kwargs={'pk': report.pk}))
    else:
        return HttpResponseBadRequest() 

@login_required
@permission_required(['reporting.view_report', 'reporting.change_report'], raise_exception=True)
def download_report(request, pk):
    """
    Download reportdefinition with X-SENDFILE header
    """
    file = Report.objects.get(pk=pk).report
    return sendfile(request, file.path, attachment=True, attachment_filename=os.path.basename(file.name))

def run_report(request, pk):
    pass