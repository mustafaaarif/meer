# Generated by Django 4.2.7 on 2023-12-14 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meerapp', '0012_uniform_lineitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lineitem',
            old_name='employee',
            new_name='uniform',
        ),
    ]
