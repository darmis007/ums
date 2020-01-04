# Generated by Django 2.2.4 on 2020-01-02 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_date_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='student_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.Student'),
        ),
        migrations.AlterField(
            model_name='student',
            name='mentor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.Volounteer'),
        ),
        migrations.AlterField(
            model_name='volounteerattendance',
            name='volounteer_name1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.Volounteer'),
        ),
    ]
