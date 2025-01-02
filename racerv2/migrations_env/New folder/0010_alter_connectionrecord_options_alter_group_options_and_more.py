# Generated by Django 4.2.17 on 2025-01-02 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('racerv2', '0009_group_remove_trackedrequest_hidden'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='connectionrecord',
            options={'ordering': ['-timestamp'], 'verbose_name': 'Connection Record', 'verbose_name_plural': 'Connection Records'},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='trackedrequest',
            options={'ordering': ['-timestamp'], 'verbose_name': 'Tracked Request', 'verbose_name_plural': 'Tracked Requests'},
        ),
    ]
