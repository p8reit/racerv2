# Generated by Django 4.2.17 on 2025-01-02 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('racerv2', '0008_merge_0007_merge_20250102_1557_fake'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('hidden', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='trackedrequest',
            name='hidden',
        ),
    ]
