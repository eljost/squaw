# Generated by Django 2.0 on 2018-01-02 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sqwbase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculation',
            name='title',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]
