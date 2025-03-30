# Generated by Django 4.2.5 on 2024-03-12 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='ФИО')),
                ('personal_id', models.CharField(blank=True, max_length=255, verbose_name='Паспорт')),
                ('driver_licence', models.CharField(blank=True, max_length=30, verbose_name='Водительское удостоверение')),
            ],
        ),
        migrations.CreateModel(
            name='Trailer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration', models.CharField(max_length=30, unique=True, verbose_name='Гос. номер')),
            ],
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration', models.CharField(max_length=30, unique=True, verbose_name='Гос. номер')),
                ('single', models.BooleanField(default=False, verbose_name='Грузовик')),
            ],
        ),
        migrations.CreateModel(
            name='TruckAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('load_max', models.DecimalField(blank=True, decimal_places=1, max_digits=3, verbose_name='Грузоподъемность')),
                ('capacity_max', models.PositiveSmallIntegerField(blank=True, max_length=3, verbose_name='Объем')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='Примечание')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logistic.driver', verbose_name='Водитель')),
                ('trailer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logistic.trailer', verbose_name='Прицеп')),
                ('truck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logistic.truck', verbose_name='Автомобиль')),
            ],
        ),
    ]
