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


# Helper for rendering a template and return it as JSON with optional parameters.
def render_ajax(request, template, context={}, additional_json={}):
    # Load template.
    template = loader.get_template(template)
    # Render template.
    renderedTemplate = template.render(context, request)

    # Create JSON dict with additional json
    json_data = additional_json
    # Add Base64 encoded template to JSON
    json_data['data'] = base64.b64encode(renderedTemplate.encode()).decode('utf-8')

    # Return JSON.
    return HttpResponse(json.dumps(json_data), 'application/json')

def generate_document_number():
    global_preferences = global_preferences_registry.manager()
    max_document_number = Transaction.objects.filter(Q(document_number_generated=True) & ~Q(document_number__startswith=global_preferences['Finance__reset_prefix'])).aggregate(Max('document_number'))['document_number__max']
    next_document_number =  '1' if max_document_number is None else str(int(max_document_number) + 1)[2:]
    return str(datetime.date.today().strftime('%y')) + next_document_number.zfill(5)

def generate_internal_number():
    max_internal_number = Transaction.objects.all().aggregate(Max('internal_number'))['internal_number__max']
    return 1 if max_internal_number is None else max_internal_number + 1