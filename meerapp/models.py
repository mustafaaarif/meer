from django.db import models
from django.contrib.auth.models import User, Group
from datetime import date
from django.utils import timezone
from django.urls import reverse
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    # Add more profile-related fields (e.g., phone number, profile picture, etc.)

    def __str__(self):
        return self.user.username
class TrialBalance(models.Model):
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
class HeadOfAccount(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
class Account(models.Model):
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=150, choices=[('current', 'Current Account'), ('savings', 'Savings Account')])
    balance = models.DecimalField(max_digits=112, decimal_places=2, default=0)

'''class Transaction(models.Model):
    TRANSACTION_MODE_CHOICES = [
        ('bank', 'Bank'),
        ('cash', 'Cash'),
    ]

    date = models.DateField(null=True, blank=True)
    head_of_accounts = models.ForeignKey(HeadOfAccount, on_delete=models.CASCADE, null=True, blank=True)
    mode = models.CharField(max_length=4, choices=TRANSACTION_MODE_CHOICES, null=True, blank=True)
    debit_account = models.ForeignKey(Account, related_name='debit_transactions', on_delete=models.CASCADE, null=True, blank=True)
    credit_account = models.ForeignKey(Account, related_name='credit_transactions', on_delete=models.CASCADE, null=True, blank=True)
    post_dated_cheque = models.BooleanField(default=False)
    cheque_number = models.CharField(max_length=20, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'Transaction #{self.id} - {self.date}'

    def save(self, *args, **kwargs):
        print(f"Transaction date: {self.date}")
        print(f"Current date: {timezone.now().date()}")
        print(f"Post-dated cheque: {self.post_dated_cheque}")

        if self.date and self.date > timezone.now().date() and not self.post_dated_cheque:
            # This transaction is in the future and is not marked as post-dated, no immediate balance update
            self.post_dated_cheque = True  # Mark as a post-dated transaction
            print(f"Post-dated transaction marked for ID #{self.id}")
        else:
            # The transaction date is today or in the past, or it is post-dated, update the balances
            self.debit_account.balance -= self.amount
            self.credit_account.balance += self.amount
            self.debit_account.save()
            self.credit_account.save()
            print(f"Balances updated for ID #{self.id}")

        super().save(*args, **kwargs)'''

class Transaction(models.Model):
    TRANSACTION_MODE_CHOICES = [
        ('bank', 'Bank'),
        ('cash', 'Cash'),
    ]

    date = models.DateField(null=True, blank=True)
    head_of_accounts = models.ForeignKey(HeadOfAccount, on_delete=models.CASCADE, null=True, blank=True)
    mode = models.CharField(max_length=4, choices=TRANSACTION_MODE_CHOICES, null=True, blank=True)
    debit_account = models.ForeignKey(Account, related_name='debit_transactions', on_delete=models.CASCADE, null=True, blank=True)
    credit_account = models.ForeignKey(Account, related_name='credit_transactions', on_delete=models.CASCADE, null=True, blank=True)
    post_dated_cheque = models.BooleanField(default=False)
    cheque_number = models.CharField(max_length=20, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'Transaction #{self.id} - {self.date}'

    def save(self, *args, **kwargs):
        # Print information for debugging
        print(f"Transaction date: {self.date}")
        print(f"Current date: {timezone.now().date()}")
        print(f"Post-dated cheque: {self.post_dated_cheque}")

        if self.date and self.date > timezone.now().date():
            # Transaction date is in the future
            self.post_dated_cheque = True
            print(f"Post-dated transaction marked for ID #{self.id}")
        else:
            # The transaction date is today or in the past, or it is already post-dated
            # Update the balances
            self.debit_account.balance -= self.amount
            self.credit_account.balance += self.amount
            # Save the updated account balances
            self.debit_account.save()
            self.credit_account.save()
            print(f"Balances updated for ID #{self.id}")

        # Call the original save method to save the transaction instance
        super().save(*args, **kwargs)
class JournalEntry(models.Model):
    date = models.DateField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    entry_name = models.CharField(max_length=200, default='no', null=True, blank=True)
    debit_amount = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0)
    credit_amount = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Update the account balance based on debit or credit amount
        if self.debit_amount:
            self.account.balance -= self.debit_amount
        elif self.credit_amount:
            self.account.balance += self.credit_amount

        # Save the updated balance
        self.account.save()
class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    guards_required = models.PositiveIntegerField(default=0)
    assigned_guards = models.ManyToManyField('Employee', blank=True)


    def __str__(self):
        return self.name
class Employee(models.Model):
    MSS_number = models.CharField(max_length=60, null=True, blank=True)
    edate = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    ecnicverification = models.CharField(max_length=40,null=True, blank=True)
    edesignation = models.CharField(max_length=40, null=True, blank=True)
    ename = models.CharField(max_length=40, null=True, blank=True)
    efathername = models.CharField(max_length=40, null=True, blank=True)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    econtact = models.CharField(max_length=40, null=True, blank=True)
    eexguard = models.CharField(max_length=40, null=True, blank=True)
    ecategory = models.CharField(max_length=40, null=True, blank=True)
    ecnicno = models.CharField(max_length=40, null=True, blank=True)
    ecnicexpirydate = models.DateField(null=True, blank=True)
    edateofbirth = models.DateField(null=True, blank=True)
    epresentaddress = models.CharField(max_length=60,null=True, blank=True)
    epermenantaddress = models.CharField(max_length=60,null=True, blank=True)
    eserviceno = models.CharField(max_length=40,null=True, blank=True)
    weapondate = models.DateField(null=True, blank=True)
    weapono = models.CharField(max_length=40, default='',null=True, blank=True)
    weaponname = models.CharField(max_length=40, default='',null=True, blank=True)
    uniformissuedate = models.DateField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    duty_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    # Image Fields
    employee_image = models.ImageField(upload_to='employee_images/', blank=True, null=True)
    weapon_picture = models.ImageField(upload_to='weapon_images/', blank=True, null=True)
    employee_card_image = models.ImageField(upload_to='card_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.ename} ({self.MSS_number})"
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    overtime_count= models.PositiveIntegerField(default=0, null=True, blank=True)
    overtime_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='overtime_attendances', null=True, blank=True)

    def __str__(self):
        return f"{self.employee} - {self.date} ({self.status})"
class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    full_days = models.PositiveIntegerField()
    half_days = models.PositiveIntegerField()
    overtime_full_day_rate = models.DecimalField(max_digits=10, decimal_places=2)  # Field for the full overtime rate
    overtime_half_day_rate = models.DecimalField(max_digits=10, decimal_places=2)  # Field for the half overtime rate

    class Meta:
        unique_together = ('employee', 'month', 'year')

    def calculate_salary(self):
        # Calculate salary based on full days, half days, overtime days, full rate, and half rate
        full_day_rate = self.overtime_full_day_rate
        half_day_rate = self.overtime_half_day_rate

        # Calculate the salary based on full days and half days
        full_day_salary = self.full_days * full_day_rate
        half_day_salary = self.half_days * half_day_rate

        # Calculate the total salary
        total_salary = (
            (self.employee.base_salary or 0) +
            full_day_salary +
            half_day_salary
        )

        return total_salary
class Weapon(models.Model):
    sr_number = models.CharField(max_length=50, null=True, blank=True)
    sn_number = models.CharField(max_length=50, null=True, blank=True)
    computerized_license_number = models.CharField(max_length=50, null=True, blank=True)
    weapon_number = models.CharField(max_length=50, null=True, blank=True)
    make_weapons = models.CharField(max_length=50, null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    weapon_purchase_from = models.CharField(max_length=100, null=True, blank=True)
    weapon_type = models.CharField(max_length=50, null=True, blank=True)
    weapon_serial_number = models.CharField(max_length=50, null=True, blank=True)
    ammu = models.CharField(max_length=50, null=True, blank=True)
    guard_name = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    update_date = models.DateField(null=True, blank=True)
    client_name = models.CharField(max_length=100, null=True, blank=True)
    guard_sign = models.ImageField(upload_to='guard_signs/', null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.weapon_number


class Uniform(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.employee)

class LineItem(models.Model):
    uniform = models.ForeignKey(Uniform, on_delete=models.CASCADE)
    uniform_product = models.TextField()
    description = models.TextField()
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.uniform)


