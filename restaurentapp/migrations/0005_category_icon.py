# Generated by Django 5.0.6 on 2024-06-14 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurentapp", "0004_mealitem_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="icon",
            field=models.TextField(default=3),
            preserve_default=False,
        ),
    ]