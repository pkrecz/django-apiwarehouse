# Generated by Django 5.1.3 on 2024-11-24 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_apiwhs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='binmodel',
            name='hu',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bin_hu', to='app_apiwhs.handlingunitmodel'),
        ),
    ]
