# Generated by Django 4.2.16 on 2024-12-05 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="shippingaddress",
            options={"verbose_name_plural": "Shipping Address"},
        ),
        migrations.RenameField(
            model_name="shippingaddress",
            old_name="address1",
            new_name="shipping_address1",
        ),
        migrations.RenameField(
            model_name="shippingaddress",
            old_name="city",
            new_name="shipping_city",
        ),
        migrations.RenameField(
            model_name="shippingaddress",
            old_name="country",
            new_name="shipping_country",
        ),
        migrations.RenameField(
            model_name="shippingaddress",
            old_name="email",
            new_name="shipping_email",
        ),
        migrations.RenameField(
            model_name="shippingaddress",
            old_name="full_name",
            new_name="shipping_full_name",
        ),
        migrations.RenameField(
            model_name="shippingaddress",
            old_name="state",
            new_name="shipping_state",
        ),
        migrations.RenameField(
            model_name="shippingaddress",
            old_name="zipcode",
            new_name="shipping_zipcode",
        ),
    ]