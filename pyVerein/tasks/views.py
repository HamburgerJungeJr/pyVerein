"""
Viewmodule for tasks app
"""
from django.http import JsonResponse
# Import views
from django.views.generic import TemplateView
# Import localization
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from dynamic_preferences.registries import global_preferences_registry

from members.models import Member, Subscription
from finance.models import Transaction, Account, CostCenter, CostObject
from utils.views import generate_document_number, generate_internal_number
import datetime
from django.db.models import Q

class TaskIndexView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """
    Index view for creditors
    """
    permission_required = 'taks.view_tasks'
    template_name = 'tasks/list.html'

@login_required
@permission_required(['taks.view_tasks', 'taks.run_tasks'])
def apply_subscriptions(request):
    """
    Generate transaction for membersubscriptions
    """

    if request.method == "POST":
        global_preferences = global_preferences_registry.manager()
        income_account = Account.objects.get(number=global_preferences['Tasks__subscription_income_account'])
        debitor_account = Account.objects.get(number=global_preferences['Tasks__subscription_debitor_account'])
        cost_center = CostCenter.objects.get(number=global_preferences['Tasks__subscription_cost_center'])
        cost_object = CostObject.objects.get(number=global_preferences['Tasks__subscription_cost_object'])
        missed_members = []
        members = [member.pk for member in Member.objects.all() if not member.is_terminated()]
        for member in Member.objects.filter(pk__in=members):
            if member.subscription and member.membership_number:
                # Determine how many subscriptions need to be applied
                transaction_count = 0
                if member.subscription.payment_frequency == Subscription.YEARLY and not Transaction.objects.filter(Q(account=global_preferences['Tasks__subscription_income_account']) & Q(text=_("Subscription - {membership_number} - {last_name}, {first_name}").format(membership_number=member.membership_number, last_name=member.last_name, first_name=member.first_name))).count():
                    transaction_count = 1
                
                if member.subscription.payment_frequency == Subscription.HALFYEARLY:
                    transaction_count = (2 - ((datetime.date.today().month - 1) // 6)) - Transaction.objects.filter(Q(account=global_preferences['Tasks__subscription_income_account']) & Q(text=_("Subscription - {membership_number} - {last_name}, {first_name}").format(membership_number=member.membership_number, last_name=member.last_name, first_name=member.first_name))).count()

                if member.subscription.payment_frequency == Subscription.QUARTERLY:
                    transaction_count = (4 - ((datetime.date.today().month - 1) // 3)) - Transaction.objects.filter(Q(account=global_preferences['Tasks__subscription_income_account']) & Q(text=_("Subscription - {membership_number} - {last_name}, {first_name}").format(membership_number=member.membership_number, last_name=member.last_name, first_name=member.first_name))).count()
      
                if member.subscription.payment_frequency == Subscription.MONTHLY:
                    transaction_count = (12 - (datetime.date.today().month - 1)) - Transaction.objects.filter(Q(account=global_preferences['Tasks__subscription_income_account']) & Q(text=_("Subscription - {membership_number} - {last_name}, {first_name}").format(membership_number=member.membership_number, last_name=member.last_name, first_name=member.first_name))).count()
            
                for i in range(0, transaction_count):
                    income_transaction = Transaction()
                    income_transaction.account = income_account
                    income_transaction.date = datetime.datetime.now()
                    income_transaction.text = _("Subscription - {membership_number} - {last_name}, {first_name}").format(membership_number=member.membership_number, last_name=member.last_name, first_name=member.first_name)
                    income_transaction.credit = member.subscription.amount
                    income_transaction.cost_center = cost_center
                    income_transaction.cost_object = cost_object


                    debitor_transaction = Transaction()
                    debitor_transaction.account = debitor_account
                    debitor_transaction.date = datetime.datetime.now()
                    debitor_transaction.text = _("Subscription - {membership_number} - {last_name}, {first_name}").format(membership_number=member.membership_number, last_name=member.last_name, first_name=member.first_name)
                    debitor_transaction.debit = member.subscription.amount

                    document_number = generate_document_number()
                    internal_number = generate_internal_number()
                    income_transaction.document_number = document_number
                    income_transaction.document_number_generated = True
                    income_transaction.internal_number = internal_number
                    debitor_transaction.document_number = document_number
                    debitor_transaction.document_number_generated = True
                    debitor_transaction.internal_number = internal_number

                    income_transaction.save()
                    debitor_transaction.save()
            else:
                missed_members.append("%s - %s, %s" % (member.membership_number, member.last_name, member.first_name))
        
        if missed_members:
            return JsonResponse({
                'state': 'Missed',
                'missed': missed_members
            })
        else:
            return JsonResponse({
                'state': 'Success'
            })
