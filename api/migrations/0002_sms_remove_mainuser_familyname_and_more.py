# Generated by Django 4.0.4 on 2022-10-31 08:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sms', models.CharField(max_length=4)),
                ('phone', models.CharField(max_length=11)),
                ('issued', models.DateTimeField(default=datetime.datetime(2022, 10, 31, 8, 56, 27, 533821))),
                ('valid', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='mainuser',
            name='familyname',
        ),
        migrations.AddField(
            model_name='mainuser',
            name='isauthenticated',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='estelam',
            name='issuedat',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 31, 8, 56, 27, 531571)),
        ),
        migrations.AlterField(
            model_name='mainuser',
            name='datejoin',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 31, 8, 56, 27, 530008)),
        ),
        migrations.AlterField(
            model_name='status',
            name='issuedat',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 31, 8, 56, 27, 532831)),
        ),
    ]
