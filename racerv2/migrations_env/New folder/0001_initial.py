# Generated by Django 4.2.17 on 2025-01-02 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrackedRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(max_length=255)),
                ('ip_address', models.CharField(max_length=45)),
                ('user_agent', models.TextField(blank=True, null=True)),
                ('referrer', models.TextField(blank=True, null=True)),
                ('geolocation', models.TextField(blank=True, null=True)),
                ('headers', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('group_name', models.CharField(blank=True, max_length=255, null=True)),
                ('hidden', models.BooleanField(default=False)),
            ],
        ),
    ]
