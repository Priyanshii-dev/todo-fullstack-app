# Generated manually – ImageField → BinaryField (store logo in DB)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0003_alter_task_options_and_more'),
    ]

    operations = [
        # Drop the old ImageField column (file path)
        migrations.RemoveField(
            model_name='task',
            name='logo',
        ),
        # Add BinaryField to store raw image bytes
        migrations.AddField(
            model_name='task',
            name='logo',
            field=models.BinaryField(blank=True, null=True),
        ),
        # Add content-type so we can serve the correct MIME type
        migrations.AddField(
            model_name='task',
            name='logo_content_type',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
