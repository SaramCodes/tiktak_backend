# Generated by Django 3.1.3 on 2020-12-29 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20201229_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
