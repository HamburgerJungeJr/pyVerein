"""
Serializer module for members
"""
from datetime import datetime

class MemberJSONSerializer:
    """
    JSON serializer for members
    """

    def serialize(self, members):
        """
        Serialize data
        """
        member_data = {
            'members': []
        }
        for member in members:
            member_data['members'].append({
                'salutation': member.get_salutation_display(),
                'last_name':member.last_name,
                'first_name': member.first_name,
                'street': member.street,
                'zipcode': member.zipcode,
                'city': member.city,
                'birthday': None if not member.birthday else datetime.strftime(member.birthday, '%Y-%m-%d'),
                'phone':member.phone,
                'mobile': member.mobile,
                'fax': member.fax,
                'email':member.email,
                'membership_number': member.membership_number,
                'joined_at': None if not member.joined_at else datetime.strftime(member.joined_at, '%Y-%m-%d'),
                'terminated_at': None if not member.terminated_at else datetime.strftime(member.terminated_at, '%Y-%m-%d'),
                'division': None if not member.division else [{
                    'name': division.name,
                } for division in member.division.all()],
                'payment_method': member.payment_method,
                'iban': member.iban,
                'bic': member.bic,
                'debit_mandate_at': None if not member.debit_mandate_at else datetime.strftime(member.debit_mandate_at, '%Y-%m-%d'),
                'debit_reference': member.debit_reference,
                'subscription': None if not member.subscription else [{
                    'name': subscription.name,
                    'amount': str(subscription.amount),
                    'payment_frequency': subscription.get_payment_frequency_display(),
                    'income_account': None if not subscription.get_income_account() else {
                        'number': subscription.get_income_account().number,
                        'name': subscription.get_income_account().name
                    },
                    'debitor_account': None if not subscription.get_debitor_account() else {
                        'number': subscription.get_debitor_account().number,
                        'name': subscription.get_debitor_account().name
                    },
                    'cost_center': None if not subscription.get_cost_center() else {
                        'number': subscription.get_cost_center().number,
                        'name': subscription.get_cost_center().name
                    },
                    'cost_object': None if not subscription.get_cost_object() else {
                        'number': subscription.get_cost_object().number,
                        'name': subscription.get_cost_object().name
                    },
                } for subscription in member.subscription.all()],
                'field_1': member.field_1,
                'field_2': member.field_2,
                'field_3': member.field_3,
                'field_4': member.field_4,
                'field_5': member.field_5
            })
        return member_data

class DivisionJSONSerializer():

    def serialize(self, divisions):
        """
        Serialize data
        """
        division_data = {
            'divisions': []
        }
        for division in divisions:
            division_data['divisions'].append({
                'name': division.name,
            })
        return division_data

class SubscriptionJSONSerializer():

    def serialize(self, subscriptions):
        """
        Serialize data
        """
        subscription_data = {
            'subscriptions': []
        }
        for subscription in subscriptions:
            subscription_data['subscriptions'].append({
                'name': subscription.name,
                'amount': str(subscription.amount),
                'payment_frequency': subscription.get_payment_frequency_display(),
                'income_account': None if not subscription.get_income_account() else {
                    'number': subscription.get_income_account().number,
                    'name': subscription.get_income_account().name
                },
                'debitor_account': None if not subscription.get_debitor_account() else {
                    'number': subscription.get_debitor_account().number,
                    'name': subscription.get_debitor_account().name
                },
                'cost_center': None if not subscription.get_cost_center() else {
                    'number': subscription.get_cost_center().number,
                    'name': subscription.get_cost_center().name
                },
                'cost_object': None if not subscription.get_cost_object() else {
                    'number': subscription.get_cost_object().number,
                    'name': subscription.get_cost_object().name
                }
            })
        return subscription_data
