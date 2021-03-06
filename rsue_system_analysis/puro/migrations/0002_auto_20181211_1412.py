# Generated by Django 2.1.2 on 2018-12-11 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puro', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tour',
            options={'ordering': ('poll', 'name'), 'verbose_name': 'Тур', 'verbose_name_plural': 'Туры'},
        ),
        migrations.AddField(
            model_name='tour',
            name='name',
            field=models.CharField(default='2', max_length=255, verbose_name='Название'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='tour',
            unique_together={('poll', 'name')},
        ),
    ]
