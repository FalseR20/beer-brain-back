# Generated by Django 4.2.4 on 2023-09-30 06:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_deposit_event_member_repayment_delete_debt_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="date",
            field=models.DateField(auto_now_add=True),
        ),
    ]
