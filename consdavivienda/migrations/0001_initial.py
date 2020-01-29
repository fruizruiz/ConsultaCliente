# Generated by Django 2.2.5 on 2019-09-26 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resumen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificacion', models.CharField(db_index=True, default='0', max_length=20)),
                ('total_oper_pendientes', models.FloatField(default='0')),
                ('total_oper_liquidadas', models.FloatField(default='0')),
                ('total_oper_anuladas', models.FloatField(default='0')),
                ('total_tran_eur', models.FloatField(default='0')),
                ('total_tran_usd', models.FloatField(default='0')),
                ('total_tran_cad', models.FloatField(default='0')),
                ('total_oper_v', models.FloatField(default='0')),
                ('total_oper_c', models.FloatField(default='0')),
                ('total_oper_j', models.FloatField(default='0')),
                ('avg_valor_usd', models.FloatField(default='0')),
                ('monto_usd_q25', models.FloatField(default='0')),
                ('monto_usd_q50', models.FloatField(default='0')),
                ('monto_usd_q75', models.FloatField(default='0')),
                ('maxim_d_sin_oper', models.FloatField(default='0')),
                ('avg_dias', models.FloatField(default='0')),
                ('max_dias_sin_transar', models.FloatField(default='0')),
                ('min_dias_sin_transar', models.FloatField(default='0')),
                ('dias_sin_transar_q25', models.FloatField(default='0')),
                ('dias_sin_transar_q50', models.FloatField(default='0')),
                ('dias_sin_transar_q75', models.FloatField(default='0')),
            ],
        ),
    ]
