# Generated by Django 2.0 on 2017-12-21 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sqwbase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='workflow',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sqwbase.Workflow'),
            preserve_default=False,
        ),
    ]
