# Generated by Django 4.2.5 on 2025-03-26 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistic', '0004_alter_driver_type_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='type_id',
            field=models.CharField(choices=[('Passport', 'Паспорт'), ('PersonalID', 'Удостоверение личности')], max_length=55, verbose_name='Документ'),
        ),
    ]
