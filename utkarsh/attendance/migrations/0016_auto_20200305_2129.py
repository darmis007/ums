# Generated by Django 2.2.4 on 2020-03-05 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0015_school_school_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='has_attended',
            field=models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent')], default='Absent', max_length=50),
        ),
    ]