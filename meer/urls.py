from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from meerapp import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from invoice.views import (
    InvoiceListView,
    createInvoice,
    view_PDF,
    generate_PDF,
    change_status,
)
from meerapp.views import UniformFormView, UniformListView

urlpatterns = [
    # Authentication
    path('', views.index_view, name='index'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/create/', views.create_account, name='create_account'),
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/<int:account_id>/', views.account_detail, name='account_detail'),
    #path('income-statement/', views.income_statement, name='income-statement'),
    #path('income_statement/', views.income_statement, name='income_statement'),
    path('balance_sheet/', views.balance_sheet, name='balance_sheet'),
    path('accounts/<int:account_id>/balance-sheet/', views.account_balance_sheet, name='account_balance_sheet'),
    path('invoices/<int:invoice_id>/', views.invoice_details, name='invoice_details'),
    path('invoices/<int:invoice_id>/create-item/', views.create_invoice_item, name='create_invoice_item'),
    path('add_journal_entry/', views.add_journal_entry, name='add_journal_entry'),
    path('accounts/trial_balance/', views.trial_balance, name='trial_balance'),
    path('journal-entries/<int:year>/<int:month>/', views.journal_entries_by_month_year, name='journal_entries_by_month_year'),
    path('add_employee/', views.add_employee, name='add_employee'),  # Add a new employee
    path('edit_employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),  # Edit an employee
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),  # Delete an employee
    path('employee_list/', views.employee_list, name='employee_list'),  # List all employees
    path('trash/', views.trash, name='trash'),
    path('restore_employee/<int:employee_id>/', views.restore_employee, name='restore_employee'),

    path('head_of_accounts/', views.head_of_accounts, name='head_of_accounts'),
    path('add_head_of_account/', views.add_head_of_account, name='add_head_of_account'),
    path('transactions/', views.transactions, name='transactions'),
    path('add_transaction/', views.add_transaction, name='add_transaction')
    ,
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('attendance-list/', views.attendance_list, name='attendance_list'),  # Add this line
    path('attendance-report/', views.attendance_report, name='attendance-report'),
    path('create_salary/', views.create_salary, name='create_salary'),
    path('list_salaries/', views.list_salaries, name='list_salaries'),
    path('calculate_salaries/', views.calculate_salaries, name='calculate_salaries'),
    path('weapons/', views.WeaponListView.as_view(), name='weapon-list'),
    path('weapons/<int:pk>/', views.WeaponDetailView.as_view(), name='weapon-detail'),
    path('weapons/add/', views.WeaponCreateView.as_view(), name='weapon-create'),
    path('location/<int:location_id>/', views.location_detail, name='location_detail'),
    path('location/<int:location_id>/assign_guards/', views.assign_guards, name='assign_guards'),
    path('location/add/', views.add_location, name='add_location'),
    path('locations/', views.location_list, name='location_list'),
    path('get_total_overtime/', views.get_total_overtime, name='get_total_overtime'),
    path('employee_report/<int:employee_id>/', views.employee_report, name='employee_report'),
    path('view_salary_detail/<int:salary_id>/', views.view_salary_detail, name='view_salary_detail'),
    path('uniform-form/', UniformFormView.as_view(), name='uniform_form'),
    path('uniform-list/', UniformListView.as_view(), name='uniform_list'),
    path('invoices/', include('invoice.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)