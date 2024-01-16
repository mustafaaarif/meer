from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from django.db import models
from .forms import TransactionForm, AccountForm, JournalEntryForm, HeadOfAccountForm
from .models import Account, Transaction, Attendance, Salary, HeadOfAccount, Uniform
from django.views.decorators.http import require_POST
from .forms import AttendanceForm, LocationForm
from django.contrib import messages
from .forms import SalaryForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Weapon, Location
from .forms import WeaponForm
from .forms import AssignGuardFormSet
from django.http import JsonResponse
def assign_guards(request, location_id):
    location = Location.objects.get(pk=location_id)

    initial_data = []
    assigned_guards = location.assigned_guards.all()

    for guard in assigned_guards:
        initial_data.append({'assigned_guard': guard})

    if request.method == "POST":
        formset = AssignGuardFormSet(request.POST, initial=initial_data)

        if formset.is_valid():
            location.assigned_guards.clear()
            for form in formset:
                assigned_guard = form.cleaned_data.get('assigned_guard')  # Use 'get' to avoid KeyError
                if assigned_guard:
                    location.assigned_guards.add(assigned_guard)
            return redirect('assign_guards', location_id=location_id)  # Redirect to the same page for further editing
    else:
        formset = AssignGuardFormSet(initial=initial_data)

    return render(request, 'assign_guards.html', {'formset': formset, 'location': location})

def location_list(request):
    locations = Location.objects.all()
    return render(request, 'location_list.html', {'locations': locations})

def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('location_list')  # Redirect to a list of all locations.
    else:
        form = LocationForm()

    return render(request, 'add_location.html', {'form': form})


def location_detail(request, location_id):
    location = Location.objects.get(id=location_id)
    assigned_guards = Employee.objects.filter(duty_location=location)

    return render(request, 'location_detail.html', {'location': location, 'assigned_guards': assigned_guards})

class WeaponCreateView(CreateView):
    model = Weapon
    template_name = 'weapon_form.html'  # Create a corresponding HTML template for the form
    form_class = WeaponForm  # Use the custom form
    success_url = '/weapons/'  # Redirect to the weapon list after successful submission
class WeaponListView(ListView):
    model = Weapon
    template_name = 'weapon_list.html'  # Create a corresponding HTML template

class WeaponDetailView(DetailView):
    model = Weapon
    template_name = 'weapon_detail.html'  # Create a corresponding HTML template
#def create_salary(request):
 #   if request.method == 'POST':
  #      form = SalaryForm(request.POST)
   #     if form.is_valid():
    #        form.save()
     #       return redirect('list_salaries')
    #else:
     #   form = SalaryForm()

    # Fetch all employees
    #employees = Employee.objects.all()

    #return render(request, 'create_salary.html', {'form': form, 'employees': employees})

def list_salaries(request):
    salaries = Salary.objects.all()
    total_salary = sum(s.calculate_salary() for s in salaries)  # Calculate the total salary amount
    return render(request, 'list_salaries.html', {'salaries': salaries, 'total_salary': total_salary})

def calculate_salaries(request):
    salaries = Salary.objects.all()
    return render(request, 'calculate_salaries.html', {'salaries': salaries})

"""
import calendar

def attendance_report(request):
    if request.method == 'GET':
        month = request.GET.get('month')
        year = request.GET.get('year')

        if month and year:
            try:
                month = int(month)
                year = int(year)
            except ValueError:
                return render(request, 'attendance_report.html', {'error_message': 'Invalid month or year'})

            employees = Employee.objects.all()

            attendance_data = {}

            for employee in employees:
                # Calculate the number of days in the specified month and year
                _, total_days = calendar.monthrange(year, month)

                present_days = Attendance.objects.filter(
                    employee=employee, date__month=month, date__year=year, status='Present'
                ).count()

                absent_days = total_days - present_days

                if total_days > 0:
                    attendance_percentage = (present_days / total_days) * 100
                else:
                    attendance_percentage = 0

                attendance_data[employee] = {
                    'total_days': total_days,
                    'present_days': present_days,
                    'absent_days': absent_days,
                    'attendance_percentage': attendance_percentage,
                }

            return render(
                request,
                'attendance_report.html',
                {'attendance_data': attendance_data, 'month': month, 'year': year},
            )

    return render(request, 'attendance_report.html')
"""

from .models import Attendance, Employee
import calendar

def attendance_report(request):
    if request.method == 'GET':
        month = request.GET.get('month')
        year = request.GET.get('year')

        if month and year:
            try:
                month = int(month)
                year = int(year)
            except ValueError:
                return render(request, 'attendance_report.html', {'error_message': 'Invalid month or year'})

            employees = Employee.objects.all()

            attendance_data = {}

            for employee in employees:
                # Calculate the number of days in the specified month and year
                _, total_days = calendar.monthrange(year, month)

                present_days = Attendance.objects.filter(
                    employee=employee, date__month=month, date__year=year, status='Present'
                ).count()

                absent_days = total_days - present_days

                if total_days > 0:
                    attendance_percentage = (present_days / total_days) * 100
                else:
                    attendance_percentage = 0

                # Calculate the total overtime for the selected month and year
                total_overtime = Attendance.objects.filter(
                    employee=employee, date__month=month, date__year=year
                ).aggregate(Sum('overtime_count'))['overtime_count__sum'] or 0

                attendance_data[employee] = {
                    'total_days': total_days,
                    'present_days': present_days,
                    'absent_days': absent_days,
                    'attendance_percentage': attendance_percentage,
                    'total_overtime': total_overtime,  # Add total overtime to the data
                }

            return render(
                request,
                'attendance_report.html',
                {'attendance_data': attendance_data, 'month': month, 'year': year},
            )

    return render(request, 'attendance_report.html')

#def create_salary(request):
 #   employees = Employee.objects.all()

  #  if request.method == 'POST':
   #    if form.is_valid():
    #        form.save()
     #       return redirect('list_salaries')
    #else:
     #   form = SalaryForm()

    # Fetch total overtime for the selected employee, month, and year
    #employee_id = request.GET.get('employee', None)
    #month = request.GET.get('month', None)
    #year = request.GET.get('year', None)

    #total_overtime = 0  # Default value if not provided

    #if employee_id and month and year:
        # Perform the logic to fetch total overtime based on the provided parameters
        #total_overtime = calculate_total_overtime(employee_id, month, year)

    #return render(request, 'create_salary.html', {'form': form, 'employees': employees, 'total_overtime': total_overtime})

def create_salary(request):
    employees = Employee.objects.all()

    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            # Check if a salary entry already exists
            employee = form.cleaned_data['employee']
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']

            existing_salary = Salary.objects.filter(employee=employee, month=month, year=year).exists()

            if existing_salary:
                return render(request, 'create_salary.html', {'form': form, 'employees': employees, 'total_overtime': 0, 'error_message': 'Salary already created for this employee in the selected month and year'})

            # Continue with the salary creation
            form.save()
            return redirect('list_salaries')
    else:
        form = SalaryForm()

    # Fetch total overtime for the selected employee, month, and year
    employee_id = request.GET.get('employee', None)
    month = request.GET.get('month', None)
    year = request.GET.get('year', None)

    total_overtime = 0  # Default value if not provided

    if employee_id and month and year:
        # Perform the logic to fetch total overtime based on the provided parameters
        total_overtime = calculate_total_overtime(employee_id, month, year)

    return render(request, 'create_salary.html', {'form': form, 'employees': employees, 'total_overtime': total_overtime})

def calculate_total_overtime(employee_id, month, year):
    try:
        employee = Employee.objects.get(id=employee_id)
        total_overtime = employee.get_total_overtime(month, year)
        return total_overtime
    except Employee.DoesNotExist:
        return 0  # Default value if employee not found
def attendance_list(request):
    # Retrieve all marked attendance records
    marked_records = Attendance.objects.all()

    return render(request, 'attendance_list.html', {'marked_records': marked_records})

def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            # Check if attendance for the same date and employee already exists
            employee = form.cleaned_data['employee']
            date = form.cleaned_data['date']
            if Attendance.objects.filter(employee=employee, date=date).exists():
                messages.error(request, 'Attendance for this employee on this date already exists.')
            else:
                form.save()
                messages.success(request, 'Attendance has been marked successfully.')
        else:
            messages.error(request, 'Failed to mark attendance. Please check the form data.')
    else:
        form = AttendanceForm()

    return render(request, 'mark_attendance.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'profile.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

def index_view(request):
    return render(request, 'index.html')



def head_of_accounts(request):
    heads_of_account = HeadOfAccount.objects.all()
    return render(request, 'head_of_accounts.html', {'heads_of_account': heads_of_account})

def add_head_of_account(request):
    if request.method == 'POST':
        form = HeadOfAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('head_of_accounts')
    else:
        form = HeadOfAccountForm()
    return render(request, 'add_head_of_account.html', {'form': form})

def transactions(request):
    transactions_list = Transaction.objects.all()
    return render(request, 'transactions.html', {'transactions_list': transactions_list})

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transactions')
    else:
        form = TransactionForm()
    return render(request, 'add_transaction.html', {'form': form})



def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account_list')
    else:
        form = AccountForm()

    return render(request, 'account_form.html', {'form': form})

'''def account_list(request):
    # Get all accounts
    accounts = Account.objects.all()

    # Calculate the updated balance for each account
    for account in accounts:
        # Sum the credit transactions
        credit_transactions = Transaction.objects.filter(credit_account=account)
        credit_amount = sum(transaction.amount for transaction in credit_transactions)

        # Sum the debit transactions
        debit_transactions = Transaction.objects.filter(debit_account=account)
        debit_amount = sum(transaction.amount for transaction in debit_transactions)

        # Calculate the updated balance
        updated_balance = account.balance + credit_amount - debit_amount

        # Update the account instance with the new balance
        account.updated_balance = updated_balance

    # Pass the updated accounts to the template
    context = {'accounts': accounts}
    return render(request, 'account_list.html', context)'''

from django.shortcuts import render
from django.db.models import Sum
from .models import Account, Transaction

def account_list(request):
    # Get all accounts
    accounts = Account.objects.all()

    # Get the current date
    current_date = timezone.now().date()

    # Calculate the updated balance for each account up to the current date
    for account in accounts:
        # Sum the credit transactions up to the current date
        credit_transactions = Transaction.objects.filter(
            credit_account=account,
            date__lte=current_date,
            post_dated_cheque=False
        )
        credit_amount = credit_transactions.aggregate(Sum('amount'))['amount__sum'] or 0

        # Sum the debit transactions up to the current date
        debit_transactions = Transaction.objects.filter(
            debit_account=account,
            date__lte=current_date,
            post_dated_cheque=False
        )
        debit_amount = debit_transactions.aggregate(Sum('amount'))['amount__sum'] or 0

        # Calculate the updated balance
        updated_balance = account.balance + credit_amount - debit_amount

        # Update the account instance with the new balance
        account.updated_balance = updated_balance

    # Pass the updated accounts to the template
    context = {'accounts': accounts}
    return render(request, 'account_list.html', context)


def account_detail(request, account_id):
    account = Account.objects.get(id=account_id)
    return render(request, 'account_detail.html', {'account': account})

#def income_statement(request):
 #   today = datetime.today()
  #  first_day_of_month = today.replace(day=1)
   # income, expenses = calculate_income_and_expenses(first_day_of_month, today)
    #net_income = income - expenses
    #context = {
        #'income': income,
        #'expenses': expenses,
        #'net_income': net_income,
    #}
    #return render(request, 'income_statement.html', context)

def balance_sheet(request):
    total_assets, total_liabilities, net_equity = generate_balance_sheet()

    # Calculate asset details
    accounts = Account.objects.all()  # Fetch all accounts
    cash_and_equivalents = accounts.filter(account_type='current').aggregate(Sum('balance'))['balance__sum'] or 0
    accounts_receivable = accounts.filter(account_type='receivable').aggregate(Sum('balance'))['balance__sum'] or 0
    inventory = accounts.filter(account_type='inventory').aggregate(Sum('balance'))['balance__sum'] or 0
    property_equipment = accounts.filter(account_type='property_equipment').aggregate(Sum('balance'))['balance__sum'] or 0
    accumulated_depreciation = accounts.filter(account_type='accumulated_depreciation').aggregate(Sum('balance'))['balance__sum'] or 0
    investments = accounts.filter(account_type='investment').aggregate(Sum('balance'))['balance__sum'] or 0
    other_assets = accounts.filter(account_type='other_assets').aggregate(Sum('balance'))['balance__sum'] or 0

    # Calculate liability and equity details
    accounts_payable = accounts.filter(account_type='accounts_payable').aggregate(Sum('balance'))['balance__sum'] or 0
    short_term_loans = accounts.filter(account_type='short_term_loans').aggregate(Sum('balance'))['balance__sum'] or 0
    accrued_expenses = accounts.filter(account_type='accrued_expenses').aggregate(Sum('balance'))['balance__sum'] or 0
    long_term_debt = accounts.filter(account_type='long_term_debt').aggregate(Sum('balance'))['balance__sum'] or 0
    other_liabilities = accounts.filter(account_type='other_liabilities').aggregate(Sum('balance'))['balance__sum'] or 0
    common_stock = accounts.filter(account_type='common_stock').aggregate(Sum('balance'))['balance__sum'] or 0
    retained_earnings = accounts.filter(account_type='retained_earnings').aggregate(Sum('balance'))['balance__sum'] or 0

    # Calculate net property, plant, equipment
    net_property_equipment = property_equipment - accumulated_depreciation

    total_current_assets = cash_and_equivalents + accounts_receivable + inventory + property_equipment + accumulated_depreciation + investments + other_assets
    total_current_liabilities = accounts_payable + short_term_loans + accrued_expenses
    total_equity = common_stock + retained_earnings
    total_liabilities_equity = total_liabilities + total_equity

    context = {
        'cash_and_equivalents': cash_and_equivalents,
        'accounts_receivable': accounts_receivable,
        'inventory': inventory,
        'property_equipment': property_equipment,
        'accumulated_depreciation': accumulated_depreciation,
        'net_property_equipment': net_property_equipment,
        'investments': investments,
        'other_assets': other_assets,
        'total_current_assets': total_current_assets,
        'accounts_payable': accounts_payable,
        'short_term_loans': short_term_loans,
        'accrued_expenses': accrued_expenses,
        'total_current_liabilities': total_current_liabilities,
        'long_term_debt': long_term_debt,
        'other_liabilities': other_liabilities,
        'common_stock': common_stock,
        'retained_earnings': retained_earnings,
        'total_equity': total_equity,
        'total_liabilities_equity': total_liabilities_equity,
    }

    return render(request, 'balance_sheet.html', context)

#def generate_balance_sheet():
    #total_assets = Account.objects.aggregate(Sum('balance'))['balance__sum'] or 0
    #total_liabilities = Transaction.objects.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    #net_equity = total_assets - total_liabilities
    #return total_assets, total_liabilities, net_equity

from django.http import Http404


def account_balance_sheet(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        raise Http404("Account does not exist")

    context = generate_balance_sheet(account)
    return render(request, 'account_balance_sheet.html', context)

def generate_balance_sheet(account):
    total_assets = account.cash_and_equivalents + account.accounts_receivable + account.inventory + account.property_equipment + account.accumulated_depreciation + account.investments + account.other_assets
    total_liabilities = account.accounts_payable + account.short_term_loans + account.accrued_expenses + account.long_term_debt + account.other_liabilities
    net_equity = total_assets - total_liabilities  # Corrected calculation for net equity
    return {
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'net_equity': net_equity,
        'account': account,
    }

# Create a new invoice
def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            return redirect('invoice_details', invoice_id=invoice.id)
    else:
        form = InvoiceForm()
    return render(request, 'create_invoice.html', {'form': form})

# View details of a specific invoice
def invoice_details(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'invoice_details.html', {'invoice': invoice})

from decimal import Decimal

def create_invoice_item(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if request.method == 'POST':
        form = InvoiceItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.invoice = invoice
            # Convert input values to Decimal if they are not empty
            item.quantity = Decimal(item.quantity) if item.quantity else Decimal(0)
            item.unit_price = Decimal(item.unit_price) if item.unit_price else Decimal(0)
            item.amount = item.quantity * item.unit_price  # Calculate the amount
            item.save()
            return redirect('invoice_details', invoice_id=invoice.id)
    else:
        form = InvoiceItemForm()
    return render(request, 'create_invoice_item.html', {'form': form, 'invoice': invoice})


def add_journal_entry(request):
    accounts = Account.objects.all()
    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trial_balance')
    else:
        form = JournalEntryForm()

    return render(request, 'add_journal_entry.html', {'accounts': accounts, 'form': form})

def trial_balance(request):
    accounts = Account.objects.all()
    trial_balance = {}
    journal_entries = JournalEntry.objects.all()  # Get all journal entries

    for account in accounts:
        debit_total = journal_entries.filter(account=account).aggregate(models.Sum('debit_amount'))['debit_amount__sum'] or 0
        credit_total = journal_entries.filter(account=account).aggregate(models.Sum('credit_amount'))['credit_amount__sum'] or 0
        balance = debit_total - credit_total
        trial_balance[account.name] = balance

    return render(request, 'trial_balance.html', {'trial_balance': trial_balance, 'journal_entries': journal_entries})

from django.shortcuts import render, get_object_or_404
from .models import TrialBalance
from .forms import TrialBalanceFilterForm

def trial_balance_view(request):
    trial_balances = []  # Initialize an empty list to hold trial balance data

    if request.method == 'POST':
        form = TrialBalanceFilterForm(request.POST)
        if form.is_valid():
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            trial_balances = TrialBalance.objects.filter(month=month, year=year)
    else:
        form = TrialBalanceFilterForm()

    context = {'form': form, 'trial_balances': trial_balances}
    return render(request, 'trial_balance_template.html', context)


from django.shortcuts import render
from .models import JournalEntry  # Import your JournalEntry model here

def journal_entries_by_month_year(request, year, month):
    # Retrieve journal entries for the specified year and month
    journal_entries = JournalEntry.objects.filter(date__year=year, date__month=month)

    context = {
        'journal_entries': journal_entries,
        'selected_month': month,
        'selected_year': year,
    }

    return render(request, 'journal_entries_by_month_year.html', context)


from django.shortcuts import render, redirect
from .models import Employee
from .forms import EmployeeForm, EmployeeUpdateForm


def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employee_list')  # Redirect to the employee list page after adding
    else:
        form = EmployeeForm()

    return render(request, 'add_employee.html', {'form': form})


def employee_list(request):
    # Query the database for employees that are not deleted
    employees = Employee.objects.filter(is_deleted=False)

    return render(request, 'employee_list.html', {'employees': employees})

def edit_employee(request, employee_id):
    # Get the employee object or return a 404 error if not found
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == 'POST':
        form = EmployeeUpdateForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')  # Redirect to the employee list page after updating
    else:
        form = EmployeeUpdateForm(instance=employee)

    return render(request, 'edit_employee.html', {'form': form, 'employee': employee})


def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == 'POST':
        # Mark the employee as deleted
        employee.is_deleted = True
        employee.save()
        # Redirect to the trash page with the deleted employee
        return render(request, 'trash.html', {'deleted_employees': [employee]})

    return render(request, 'delete_employee.html', {'employee': employee})


def trash(request):
    # Query the database for deleted employees
    deleted_employees = Employee.objects.filter(is_deleted=True)

    return render(request, 'trash.html', {'deleted_employees': deleted_employees})

@require_POST
def restore_employee(request, employee_id):
    # Retrieve the deleted employee by their ID
    deleted_employee = get_object_or_404(Employee, id=employee_id)

    # Restore the employee by setting is_deleted to False
    deleted_employee.is_deleted = False
    deleted_employee.save()

    # Redirect back to the trash or employee list, depending on your preference
    # For example, if you want to redirect to the trash list:
    #return redirect('trash/')

    # If you want to redirect to the employee list:
    return redirect('employee_list')

# views.py

from django.db.models import Sum

def get_total_overtime(request):
    if request.method == 'GET':
        employee_id = request.GET.get('employee_id')
        month = request.GET.get('month')
        year = request.GET.get('year')

        if employee_id and month and year:
            try:
                employee = Employee.objects.get(id=employee_id)
                month = int(month)
                year = int(year)

                total_overtime = Attendance.objects.filter(
                    employee=employee, date__month=month, date__year=year
                ).aggregate(Sum('overtime_count'))['overtime_count__sum'] or 0

                return JsonResponse({'total_overtime': total_overtime})
            except Employee.DoesNotExist:
                return JsonResponse({'error': 'Employee not found'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def employee_report(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    return render(request, 'employee_report.html', {'employee': employee})


def view_salary_detail(request, salary_id):
    salary = get_object_or_404(Salary, pk=salary_id)
    return render(request, 'salary_detail.html', {'salary': salary})


# views.py
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import UniformForm, LineItemFormSet

from django.urls import reverse

class UniformFormView(FormView):
    template_name = 'uniform_form.html'
    form_class = UniformForm
    success_url = 'uniform_list'

    def form_valid(self, form):
        uniform_instance = form.save()
        lineitem_formset = LineItemFormSet(self.request.POST, instance=uniform_instance)

        if lineitem_formset.is_valid():
            lineitem_formset.save()

            return redirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form, lineitem_formset=lineitem_formset))

    def get_success_url(self):
        return reverse(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lineitem_formset'] = LineItemFormSet()
        return context


from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import FormView
from .models import Uniform, LineItem
from .forms import UniformForm, LineItemFormSet

class UniformListView(ListView):
    model = Uniform
    template_name = 'uniform_list.html'
    context_object_name = 'uniforms'

