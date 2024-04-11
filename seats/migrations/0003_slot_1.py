# Generated by Django 5.0.3 on 2024-04-11 09:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("seats", "0002_alter_entry_adm_no"),
    ]

    operations = [
        migrations.CreateModel(
            name="Slot_1",
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
                ("seat_1", models.CharField(max_length=2)),
                ("seat_2", models.CharField(max_length=2)),
                ("adm_no", models.CharField(max_length=6)),
            ],
        ),
    ]