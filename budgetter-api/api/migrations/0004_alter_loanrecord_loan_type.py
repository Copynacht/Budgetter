# Generated by Django 5.2.1 on 2025-05-31 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_loanrecord_loan_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanrecord',
            name='loan_type',
            field=models.IntegerField(choices=[(0, '貸した'), (1, '借りた')]),
        ),
    ]
