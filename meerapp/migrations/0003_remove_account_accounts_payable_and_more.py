# Generated by Django 4.2.7 on 2023-11-26 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meerapp', '0002_alter_account_id_alter_attendance_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='accounts_payable',
        ),
        migrations.RemoveField(
            model_name='account',
            name='accounts_receivable',
        ),
        migrations.RemoveField(
            model_name='account',
            name='accrued_expenses',
        ),
        migrations.RemoveField(
            model_name='account',
            name='accumulated_depreciation',
        ),
        migrations.RemoveField(
            model_name='account',
            name='cash_and_equivalents',
        ),
        migrations.RemoveField(
            model_name='account',
            name='common_stock',
        ),
        migrations.RemoveField(
            model_name='account',
            name='inventory',
        ),
        migrations.RemoveField(
            model_name='account',
            name='investments',
        ),
        migrations.RemoveField(
            model_name='account',
            name='long_term_debt',
        ),
        migrations.RemoveField(
            model_name='account',
            name='other_assets',
        ),
        migrations.RemoveField(
            model_name='account',
            name='other_liabilities',
        ),
        migrations.RemoveField(
            model_name='account',
            name='property_equipment',
        ),
        migrations.RemoveField(
            model_name='account',
            name='retained_earnings',
        ),
        migrations.RemoveField(
            model_name='account',
            name='short_term_loans',
        ),
    ]
