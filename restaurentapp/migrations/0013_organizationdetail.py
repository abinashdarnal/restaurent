# Generated by Django 5.0.6 on 2024-06-20 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurentapp", "0012_alter_mealitem_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrganizationDetail",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(blank=True, max_length=400, null=True)),
                ("address", models.CharField(blank=True, max_length=400, null=True)),
                ("phone", models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
    ]
