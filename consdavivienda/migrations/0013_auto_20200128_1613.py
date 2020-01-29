# Generated by Django 2.2.5 on 2020-01-28 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consdavivienda', '0012_auto_20200128_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resumeninfopersonajuridica',
            name='total_activos',
            field=models.CharField(default='0', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='resumeninfopersonajuridica',
            name='total_egresos',
            field=models.CharField(default='0', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='resumeninfopersonajuridica',
            name='total_ingresos',
            field=models.CharField(default='0', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='resumeninfopersonajuridica',
            name='total_pasivos',
            field=models.CharField(default='0', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='resumenproductosusuario',
            name='nombre_producto',
            field=models.CharField(default='NA', max_length=100, null=True),
        ),
    ]
