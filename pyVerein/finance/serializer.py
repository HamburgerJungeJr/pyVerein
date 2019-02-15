"""
Serializer module for finance
"""
from datetime import datetime

class AccountJSONSerializer:
    """
    JSON serializer for accounts
    """

    def serialize(self, accounts):
        """
        Serialize data
        """
        account_data = {
            'accounts': []
        }
        for account in accounts:
            account_data['accounts'].append({
                'number': account.number,
                'name': account.name,
                'account_type': account.get_account_type_display()
            })
        return account_data

class CostCenterJSONSerializer:
    """
    JSON serializer for cost centers
    """

    def serialize(self, cost_centers):
        """
        Serialize data
        """
        cost_center_data = {
            'cost_centers': []
        }
        for cost_center in cost_centers:
            cost_center_data['cost_centers'].append({
                'number': cost_center.number,
                'name': cost_center.name,
                'description': cost_center.description
            })
        return cost_center_data

class CostObjectJSONSerializer:
    """
    JSON serializer for cost objects
    """

    def serialize(self, cost_objects):
        """
        Serialize data
        """
        cost_object_data = {
            'cost_objects': []
        }
        for cost_object in cost_objects:
            cost_object_data['cost_objects'].append({
                'number': cost_object.number,
                'name': cost_object.name,
                'description': cost_object.description
            })
        return cost_object_data

class TransactionJSONSerializer:
    """
    JSON serializer for transactions
    """

    def serialize(self, transactions):
        """
        Serialize data
        """
        transaction_data = {
            'transactions': []
        }
        for transaction in transactions:
            transaction_data['transactions'].append({
                    'account': {
                        'number': transaction.account.number,
                        'name': transaction.account.name,
                        'account_type': transaction.account.get_account_type_display()
                    },
                    'date': datetime.strftime(transaction.date, '%Y-%m-%d'),
                    'document_number': transaction.document_number,
                    'text': transaction.text,
                    'debit': None if not transaction.debit else str(transaction.debit),
                    'credit': None if not transaction.credit else str(transaction.credit),
                    'cost_center': None if not transaction.cost_center else {
                        'number': transaction.cost_center.number,
                        'name': transaction.cost_center.name
                    },
                    'cost_object': None if not transaction.cost_object else {
                        'number': transaction.cost_object.number,
                        'name': transaction.cost_object.name
                    },
                    'document_number_generated': transaction.document_number_generated,
                    'internal_number': transaction.internal_number,
                    'reset': transaction.reset,
                    'clearing_number': transaction.clearing_number,
                    'accounting_year': transaction.accounting_year,
            })
        return transaction_data

class ClosureTransactionJSONSerializer:
    """
    JSON serializer for closure_transactions
    """

    def serialize(self, closure_transactions):
        """
        Serialize data
        """
        closure_transaction_data = {
            'closure_transactions': []
        }
        for closure_transaction in closure_transactions:
            closure_transaction_data['closure_transactions'].append({
                'account_number': closure_transaction.account_number,
                'account_name': closure_transaction.account_name,
                'date': datetime.strftime(closure_transaction.date, '%Y-%m-%d'),
                'document_number': closure_transaction.document_number,
                'text': closure_transaction.text,
                'debit': str(closure_transaction.debit),
                'credit': str(closure_transaction.credit),
                'cost_center_number': closure_transaction.cost_center_number,
                'cost_center_name': closure_transaction.cost_center_name,
                'cost_center_description': closure_transaction.cost_center_description,
                'cost_object_number': closure_transaction.cost_object_number,
                'cost_object_name': closure_transaction.cost_object_name,
                'cost_object_description': closure_transaction.cost_object_description,
                'document_number_generated': closure_transaction.document_number_generated,
                'internal_number': closure_transaction.internal_number,
                'reset': closure_transaction.reset,
                'clearing_number': closure_transaction.clearing_number,
                'accounting_year': closure_transaction.accounting_year,
            })
        return closure_transaction_data

class ClosureBalanceJSONSerializer:
    """
    JSON serializer for closure balances
    """

    def serialize(self, closure_balances):
        """
        Serialize data
        """
        closure_balance_data = {
            'closure_balances': []
        }
        for closure_balance in closure_balances:
            closure_balance_data['closure_balances'].append({
                'year': closure_balance.year,
                'claims': str(closure_balance.claims),
                'liabilities': str(closure_balance.liabilities)
            })
        return closure_balance_data