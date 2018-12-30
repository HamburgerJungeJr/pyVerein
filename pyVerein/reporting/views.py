# Import reverse.
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
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
from pyreportjasper import JasperPy
from pyreportjasper.jasperpy import FORMATS as JASPER_FORMATS

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
        context['models'] = [val for key, val in Report.MODELS if key in self.object.model]

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

@login_required
@permission_required(['reporting.view_report', 'reporting.run_report'], raise_exception=True)
def run_report(request, pk):
    """
    Run report and return generated file
    """
    # Get report definition
    report = Report.objects.get(pk=pk)
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
        return sendfile(request, output_filepath + '.' + file_format)
    else:
        return HttpResponseBadRequest()