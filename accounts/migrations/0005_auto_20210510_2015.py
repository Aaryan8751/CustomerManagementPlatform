# Generated by Django 3.1.2 on 2021-05-10 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210510_2012'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tags',
            new_name='Tag',
        ),
    ]
