from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages

# Create your views here.
@login_required
def index(request):
    return render(request, 'app/dashboard.html', {})
