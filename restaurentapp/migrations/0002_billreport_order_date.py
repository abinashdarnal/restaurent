# Generated by Django 5.0.6 on 2024-06-22 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurentapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='billreport',
            name='order_date',
            field=models.CharField(default=2, max_length=30),
            preserve_default=False,
        ),
    ]
