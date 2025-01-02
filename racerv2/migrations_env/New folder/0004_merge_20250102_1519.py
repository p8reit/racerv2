from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('racerv2', '0003_group_remove_trackedrequest_group_name_and_more'),  # Adjust dependency if necessary
    ]

    operations = [
        migrations.AddField(
            model_name='trackedrequest',
            name='group',
            field=models.ForeignKey(
                to='racerv2.Group',
                on_delete=models.CASCADE,
                null=True,
            ),
        ),
        migrations.RemoveField(
            model_name='trackedrequest',
            name='group_name',
        ),
    ]
