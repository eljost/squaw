# Generated by Django 2.0 on 2018-01-17 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sqwbase', '0011_auto_20180117_0619'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculation',
            name='result',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
