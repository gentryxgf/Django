# Generated by Django 2.2 on 2022-12-02 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='blogtype',
            new_name='blog_type',
        ),
        migrations.RenameField(
            model_name='blog',
            old_name='last_update_time',
            new_name='last_updated_time',
        ),
    ]