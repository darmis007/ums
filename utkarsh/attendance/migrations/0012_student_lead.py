# Generated by Django 2.2.4 on 2020-03-03 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0011_auto_20200304_0152'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='volounteer_lead', to='attendance.Volounteer'),
        ),
    ]
