# Generated by Django 2.2.4 on 2020-01-07 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0008_auto_20200107_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='on_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
