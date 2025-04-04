# Generated by Django 4.2.5 on 2023-11-07 00:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_rename_full_name_individual_formal_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='individual',
            name='partner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='individual', to='crm.company'),
        ),
        migrations.AddField(
            model_name='legal',
            name='partner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='legal', to='crm.company'),
        ),
        migrations.AddField(
            model_name='person',
            name='partner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person', to='crm.company'),
        ),
    ]
