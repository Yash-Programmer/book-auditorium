# Generated by Django 4.2.11 on 2024-04-12 10:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("seats", "0005_slot_2_slot_3_entry_slot"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entry",
            name="slot",
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
    ]
