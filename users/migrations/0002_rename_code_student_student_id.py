# Generated by Django 5.0.4 on 2024-05-05 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='code',
            new_name='student_id',
        ),
    ]
