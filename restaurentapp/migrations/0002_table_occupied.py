# Generated by Django 5.0.6 on 2024-06-14 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurentapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="table",
            name="occupied",
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]