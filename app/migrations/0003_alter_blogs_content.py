# Generated by Django 5.0.2 on 2024-03-01 09:30

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_blogs_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]
