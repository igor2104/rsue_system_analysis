# Generated by Django 2.1.2 on 2018-12-11 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functional_completeness', '0004_auto_20181211_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='function',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='object',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
    ]
