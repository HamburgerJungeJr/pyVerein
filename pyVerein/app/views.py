from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Count, Sum
from members.models import Member
from finance.models import Transaction, CostCenter, CostObject
from dynamic_preferences.registries import global_preferences_registry

# Create your views here.
@login_required
def index(request):
    global_preferences = global_preferences_registry.manager()

    members = [member.pk for member in Member.objects.all() if not member.is_terminated()]
    divisions = Member.objects.filter(pk__in=members).values('division__name').annotate(members=Count('id'))

    bank_account_pref = global_preferences['Dashboard__bank_accounts'].split(',')
    bank_accounts = Transaction.objects.filter(account__in=bank_account_pref).order_by('account__number').values('account__name').annotate(debit=Sum('debit'), credit=Sum('credit'))

    cost_center = CostCenter.objects.order_by('number').values('name').annotate(debit=Sum('transaction__debit'), credit=Sum('transaction__credit'))

    cost_object = CostObject.objects.order_by('number').values('name').annotate(debit=Sum('transaction__debit'), credit=Sum('transaction__credit'))

    return render(request, 'app/dashboard.html', {'divisions': divisions, 'bank_accounts': bank_accounts, 'cost_center': cost_center, 'cost_object': cost_object})
