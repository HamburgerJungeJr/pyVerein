# Import HttpResponse
from django.http import HttpResponse
# Import template loader.
from django.template import loader
# Import JSON
import json
# Import Base64
import base64

from finance.models import Transaction
import datetime
from dynamic_preferences.registries import global_preferences_registry
from django.db.models import Q, Max
from django.views import generic

class DetailView(generic.DetailView):

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        context['instance'] = self.object

        history = []
        for record in self.object.history.all():
            entry = {
                'type': record.history_type,
                'date': record.history_date,
                'user': record.history_user.get_full_name() if record.history_user else None,
                'changes': []
            }
            
            if record.prev_record:
                delta = record.diff_against(record.prev_record)
                for change in delta.changes:
                    entry['changes'].append({
                        'field': change.field,
                        'old': change.old,
                        'new': change.new
                    })

            history.append(entry)

        context['history'] = history

        return context

def generate_document_number():
    global_preferences = global_preferences_registry.manager()
    max_document_number = Transaction.objects.filter(Q(document_number_generated=True) & ~Q(document_number__startswith=global_preferences['Finance__reset_prefix']) & Q(accounting_year=global_preferences['Finance__accounting_year'])).aggregate(Max('document_number'))['document_number__max']
    next_document_number =  '1' if max_document_number is None else str(int(max_document_number) + 1)[2:]
    return global_preferences['Finance__accounting_year'][2:] + next_document_number.zfill(5)

def generate_internal_number():
    max_internal_number = Transaction.objects.all().aggregate(Max('internal_number'))['internal_number__max']
    return 1 if max_internal_number is None else max_internal_number + 1