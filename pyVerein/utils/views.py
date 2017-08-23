# Import HttpResponse
from django.http import HttpResponse
# Import template loader.
from django.template import loader
# Import JSON
import json
# Import Base64
import base64


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