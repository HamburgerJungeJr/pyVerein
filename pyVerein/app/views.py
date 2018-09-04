from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Count, Sum
from members.models import Member
from finance.models import Transaction
from dynamic_preferences.registries import global_preferences_registry

# Create your views here.
@login_required
def index(request):
    global_preferences = global_preferences_registry.manager()

    divisions = Member.objects.values('division__name').annotate(members=Count('id'))

    bank_account_pref = global_preferences['Dashboard__bank_accounts'].split(',')
    bank_accounts = Transaction.objects.filter(account__in=bank_account_pref).values('account__name').annotate(debit=Sum('debit'), credit=Sum('credit')).annotate

    return render(request, 'app/dashboard.html', {'divisions': divisions, 'bank_accounts': bank_accounts})
