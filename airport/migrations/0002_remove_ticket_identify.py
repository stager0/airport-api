# Generated by Django 5.2.1 on 2025-05-30 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("airport", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ticket",
            name="identify",
        ),
    ]
