from django.core.management.base import BaseCommand
from accounting.models import AccountType, Account

class Command(BaseCommand):
    help = 'Creates initial account types and accounts'

    def handle(self, *args, **options):
        # Create account types
        asset_type = AccountType.objects.create(name='Asset')
        liability_type = AccountType.objects.create(name='Liability')
        equity_type = AccountType.objects.create(name='Equity')
        revenue_type = AccountType.objects.create(name='Revenue')
        expense_type = AccountType.objects.create(name='Expense')

        # Create top-level accounts
        cash_account = Account.objects.create(name='Cash', account_type=asset_type)
        equity_account = Account.objects.create(name='Equity', account_type=equity_type)

        # Create child accounts
        checking_account = Account.objects.create(name='Checking Account', account_type=asset_type, parent=cash_account)
        savings_account = Account.objects.create(name='Savings Account', account_type=asset_type, parent=cash_account)

        self.stdout.write(self.style.SUCCESS('Successfully created initial account types and accounts'))
