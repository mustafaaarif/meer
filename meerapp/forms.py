from django import forms
from .models import Salary, Weapon, Transaction, Account, Employee, JournalEntry, Attendance, Location, HeadOfAccount
from django.forms.widgets import DateInput
from django import forms
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from .models import Employee, Location

class AssignGuardForm(forms.Form):
    assigned_guard = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        widget=forms.Select(attrs={'class': 'select2'}),
        required=False,
    )

AssignGuardFormSet = formset_factory(AssignGuardForm, extra=1)


class WeaponForm(forms.ModelForm):
    class Meta:
        model = Weapon
        fields = '__all__'
        widgets = {
            'purchase_date': DateInput(attrs={'type': 'date'}),
            'update_date': DateInput(attrs={'type': 'date'}),
        }
class HeadOfAccountForm(forms.ModelForm):
    class Meta:
        model = HeadOfAccount
        fields = ['name']
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['date', 'account', 'entry_name', 'debit_amount', 'credit_amount']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        debit_amount = cleaned_data.get('debit_amount')
        credit_amount = cleaned_data.get('credit_amount')

        if not (debit_amount or credit_amount):
            raise forms.ValidationError("Either debit amount or credit amount must be provided, but not both.")

        if debit_amount and credit_amount:
            raise forms.ValidationError("You can provide either debit amount or credit amount, not both.")

        return cleaned_data

class TrialBalanceFilterForm(forms.Form):
    month = forms.IntegerField(label='Month')
    year = forms.IntegerField(label='Year')

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"  # Include all fields from the Employee model
        widgets = {
            'ecnicexpirydate': forms.DateInput(attrs={'type': 'date'}),
            'edateofbirth': forms.DateInput(attrs={'type': 'date'}),
            'weapondate': forms.DateInput(attrs={'type': 'date'}),
            'uniformissuedate': forms.DateInput(attrs={'type': 'date'}),
        }

class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"  # Include all fields from the Employee model

        # Exclude fields that should not appear in the form
        exclude = ['ecnicexpirydate', 'edateofbirth', 'weapondate', 'uniformissuedate']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = [
            'employee',
            'month',
            'year',
            'full_days',
            'half_days',
            'overtime_full_day_rate',
            'overtime_half_day_rate',
        ]

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address', 'guards_required']

from django import forms
from django.forms import inlineformset_factory
from .models import Uniform, LineItem

class UniformForm(forms.ModelForm):
    class Meta:
        model = Uniform
        fields = ['employee', 'date', 'due_date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

LineItemFormSet = inlineformset_factory(Uniform, LineItem, fields=['uniform_product', 'description', 'quantity'], extra=1, can_delete=True)


