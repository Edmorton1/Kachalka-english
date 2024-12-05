# Generated by Django 5.1.2 on 2024-11-14 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0004_user_alter_statistic_options_alter_records_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='link',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='user',
            name='title',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Имя'),
        ),
    ]
