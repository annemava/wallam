# Generated by Django 5.1.2 on 2024-12-14 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='urgent',
            field=models.BooleanField(default=False),
        ),
    ]
