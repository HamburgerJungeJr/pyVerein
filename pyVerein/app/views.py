from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Count
from members.models import Division

# Create your views here.
@login_required
def index(request):
    divisions = Division.objects.annotate(members=Count('member'))
    return render(request, 'app/dashboard.html', {'divisions': divisions})
