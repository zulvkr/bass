# Generated by Django 3.2.4 on 2021-07-03 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210703_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=1000, null=True),
        ),
    ]
