# Generated by Django 4.2.16 on 2024-12-14 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0005_order_date_shipped"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="invoice",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="paid",
            field=models.BooleanField(default=False),
        ),
    ]
