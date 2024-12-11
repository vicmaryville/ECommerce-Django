# Generated by Django 4.2.16 on 2024-12-04 01:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Store", "0004_alter_category_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("address1", models.CharField(blank=True, max_length=200)),
                ("address2", models.CharField(blank=True, max_length=200)),
                ("city", models.CharField(blank=True, max_length=50)),
                ("state", models.CharField(blank=True, max_length=20)),
                ("zipcode", models.CharField(blank=True, max_length=20)),
                ("country", models.CharField(blank=True, max_length=20)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]