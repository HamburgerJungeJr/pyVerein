# Import django render shortcut
from django.shortcuts import render

# Index-View
def index(request):
    #Set Context
    context = {}
    # Return rendered template.
    return render(request, 'members/index.html', context)
