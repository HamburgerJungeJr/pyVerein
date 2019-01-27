# Import reverse.
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.db import Error
# Import Report.
from .forms import ReportForm, ResourceForm
from .models import Report, Resource
from members.models import Member, Division, Subscription
from members.serializer import MemberJSONSerializer, DivisionJSONSerializer, SubscriptionJSONSerializer
from finance.models import Transaction, Account, CostCenter, CostObject, ClosureBalance, ClosureTransaction
from finance.serializer import TransactionJSONSerializer, AccountJSONSerializer, CostCenterJSONSerializer, CostObjectJSONSerializer, ClosureBalanceJSONSerializer, ClosureTransactionJSONSerializer
import os
from django.conf import settings

# Import localization
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from sendfile import sendfile
import io
import uuid
import json
from pyreportjasper.jasperpy import JasperPy, FORMATS as JASPER_FORMATS
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

# Index-View.
class ReportIndexView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'reporting.view_report'
    template_name = 'reporting/list.html'

    def get_context_data(self, **kwargs):
        context = super(ReportIndexView, self).get_context_data(**kwargs)

        reports = Report.objects.all()
        context['reports'] = [report for report in reports if report.is_access_granted(self.request.user)]

        return context


# Detail-View.
class ReportDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'reporting.view_report'
    model = Report
    context_object_name = 'report'
    template_name = 'reporting/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ReportDetailView, self).get_context_data(**kwargs)

        context['resources'] = Resource.objects.filter(report=self.object)
        context['models'] = [val for key, val in Report.MODELS if key in self.object.model]

        return context

    def has_permission(self):
        super_perm = super(ReportDetailView, self).has_permission()
        return super_perm and Report.objects.get(pk=self.kwargs['pk']).is_access_granted(self.request.user)

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
    
    def has_permission(self):
        super_perm = super(ReportEditView, self).has_permission()
        return super_perm and Report.objects.get(pk=self.kwargs['pk']).is_access_granted(self.request.user)

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
        report = Report.objects.get(pk=pk)

        # Check if user can access report
        if not report.is_access_granted(request.user):
            return HttpResponseForbidden()

        try:
            resource = Resource(report=report, resource=request.FILES['resource'])
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

        # Check if user can access report
        if not report.is_access_granted(request.user):
            return HttpResponseForbidden()

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
    report = Report.objects.get(pk=pk)
    # Check if user can access report
    if not report.is_access_granted(request.user):
        return HttpResponseForbidden()

    file = report.report
    return sendfile(request, file.path, attachment=True, attachment_filename=os.path.basename(file.name))

@login_required
@permission_required(['reporting.view_report', 'reporting.run_report'], raise_exception=True)
def run_report(request, pk):
    """
    Run report and return generated file
    """
    report = Report.objects.get(pk=pk)
    # Check if user can access report
    if not report.is_access_granted(request.user):
        return HttpResponseForbidden()
    
    # Get report definition
    report_definition = report.report.path
    jasperpy = JasperPy()
    parameters = jasperpy.list_parameters(report_definition).keys()
    if request.method == 'GET':
        context = {
            'report': report,
            'parameters': parameters,
            'formats': JASPER_FORMATS,
        }
        return render(request, 'reporting/run.html', context)
        
    
    if request.method == 'POST':
        # Get POST-Parameter
        parameter_map = {}
        for param in parameters:
            val = request.POST.get(param, None)
            if not val:
                return HttpResponseBadRequest()
            parameter_map.update({
                param: val
            })
        file_format = request.POST.get('format', None)
        if not file_format:
            return HttpResponseBadRequest()
        # Create data-JSON file
        modelmap = {
            'MEM': {
                'model': Member,
                'serializer': MemberJSONSerializer,
            },
            'DIV': {
                'model': Division,
                'serializer': DivisionJSONSerializer,
            },
            'SUB': {
                'model': Subscription,
                'serializer': SubscriptionJSONSerializer,
            },
            'ACC': {
                'model': Account,
                'serializer': AccountJSONSerializer,
            },
            'COC': {
                'model': CostCenter,
                'serializer': CostCenterJSONSerializer,
            },
            'COO': {
                'model': CostObject,
                'serializer': CostObjectJSONSerializer,
            },
            'TRA': {
                'model': Transaction,
                'serializer': TransactionJSONSerializer,
            },
            'CTR': {
                'model': ClosureTransaction,
                'serializer': ClosureTransactionJSONSerializer,
            },
            'CBA': {
                'model': ClosureBalance,
                'serializer': ClosureBalanceJSONSerializer,
            }
        }
        json_data = {}
        for model in set(report.model):
            json_data.update(modelmap[model]['serializer']().serialize(modelmap[model]['model'].objects.all()))
        # Write JSON-data
        data_filepath = os.path.join(settings.MEDIA_ROOT, "protected/reports/{}/data/{}".format(report.uuid, str(uuid.uuid4()) + '.json'))
        os.makedirs(os.path.dirname(data_filepath), exist_ok=True)
        with io.open(data_filepath, 'w', encoding='utf8') as f:
            f.write(json.dumps(json_data))
        
        # Output file
        output_filepath = os.path.join(settings.MEDIA_ROOT, "protected/reports/{}/output/{}-{}".format(report.uuid, report.name, str(uuid.uuid4())))
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        try:
            jasperpy.process(
                input_file=report_definition,
                output_file=output_filepath,
                format_list=[file_format],
                db_connection={
                    'driver': 'jsonql',
                    'data_file': data_filepath,
                    'jsonql_query': report.jsonql_query
                },
                resource=os.path.join(settings.MEDIA_ROOT, 'protected/reports/{}/resource/'.format(report.uuid)),
                parameters=parameter_map
            )
        except NameError as err:
            messages.error(request, err)
            return HttpResponseRedirect(reverse_lazy('reporting:run', kwargs={'pk': pk}))

        return sendfile(request, output_filepath + '.' + file_format)
    else:
        return HttpResponseBadRequest()