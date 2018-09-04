from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Count
from members.models import Member

# Create your views here.
@login_required
def index(request):
    divisions = Member.objects.values('division__name').annotate(members=Count('id'))
    return render(request, 'app/dashboard.html', {'divisions': divisions})
