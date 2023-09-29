# Generated by Django 4.2.4 on 2023-09-29 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("beer_brain_core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Deposit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.DecimalField(decimal_places=2, max_digits=12)),
                ("description", models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(auto_now=True)),
                ("description", models.CharField(max_length=256)),
                ("is_closed", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="Member",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="beer_brain_core.event",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="beer_brain_core.user",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Repayment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.DecimalField(decimal_places=2, max_digits=12)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="beer_brain_core.event",
                    ),
                ),
                (
                    "payer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payer_member_id",
                        to="beer_brain_core.member",
                    ),
                ),
                (
                    "recipient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recipient_member_id",
                        to="beer_brain_core.member",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Debt",
        ),
        migrations.AddField(
            model_name="deposit",
            name="member",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="beer_brain_core.member"
            ),
        ),
    ]