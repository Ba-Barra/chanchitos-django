# Generated by Django 5.0.6 on 2024-06-27 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0007_envio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='image',
            new_name='imagen',
        ),
    ]
