# Generated by Django 4.2.4 on 2023-09-30 07:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("beer_brain_core", "0003_alter_event_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="is_closed",
            field=models.BooleanField(default=False),
        ),
    ]
