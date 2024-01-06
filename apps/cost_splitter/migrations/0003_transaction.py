# Generated by Django 5.0 on 2024-01-03 19:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cost_splitter', '0002_remove_cost_excluded_amount_alter_cost_description_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('creditor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='credit_transactions', to=settings.AUTH_USER_MODEL)),
                ('debtor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='debit_transactions', to=settings.AUTH_USER_MODEL)),
                ('included_in_report', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cost_splitter.costsplitreport')),
            ],
        ),
    ]