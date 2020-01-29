from .models import Resumen
from rest_framework import serializers

class ResumenSerializer(serializers.ModelSerializer):
	class Meta:
		model = Resumen
		fields = [
		'identificacion','total_oper_pendientes','total_oper_liquidadas','total_oper_anuladas','total_tran_eur','total_tran_usd',
		'total_tran_cad','total_oper_v','total_oper_c',
		'total_oper_j','avg_valor_usd','monto_usd_q25','monto_usd_q50',
		'monto_usd_q75',
		'maxim_d_sin_oper',
		'avg_dias',
		'max_dias_sin_transar',
		'min_dias_sin_transar',
		'dias_sin_transar_q25',
		'dias_sin_transar_q50',
		'dias_sin_transar_q75',
		'tipo_identificacion',
		'primer_apellido',
		'segundo_apellido',
		'nombre',
		'fecha_nacimiento',
		'estado',
		'direccion',
		'ciudad',
		'pais',
		'celular',
		'email',
		'telefono','cod_tipo_id'
		]