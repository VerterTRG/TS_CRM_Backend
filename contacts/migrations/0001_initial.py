# Generated by Django 5.1.7 on 2025-04-06 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('phone', models.CharField(max_length=150, verbose_name='Телефон')),
                ('email', models.CharField(blank=True, max_length=150, verbose_name='Эл. почта')),
            ],
            options={
                'db_table': 'contact_list',
            },
        ),
    ]
