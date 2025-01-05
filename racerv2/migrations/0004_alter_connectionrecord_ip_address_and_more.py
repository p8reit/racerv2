# Generated by Django 4.2.17 on 2025-01-05 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('racerv2', '0003_connectionrecord_is_google_hosted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectionrecord',
            name='ip_address',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='trackedrequest',
            name='ip_address',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]