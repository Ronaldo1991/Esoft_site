# Generated by Django 2.2.4 on 2022-02-16 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20220216_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusuario',
            name='id',
            field=models.CharField(default='1f515fe8-3b63-468c-9fc3-4d3adfceb2e1', max_length=36, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
