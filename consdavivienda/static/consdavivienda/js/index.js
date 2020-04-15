	function ajaxCall() {
	var id = $("#identificacion").val();
    $.getJSON("/consdavivienda/sugiereIdentificacion/"+id+"/",
        function(data) {
			console.log(data)
		$.each(data, function(k, v) {    
             alert(k);		
			 alert(v.fields.identificacion);
        });
    });        
}

    $('#identificacion').autocomplete({
		source:  function (request, response) {
        $.getJSON("/consdavivienda/sugiereIdentificacion/"+$("#identificacion").val()+"/", function (data) {
			response($.map(data, function (value, key) {
                return {
                    label: value.fields.identificacion+" "+value.fields.nombre,
                    value: value.fields.identificacion
                };
            }));
        });
        },
		minLength: 4,
		delay: 100
    });
	
function test() {
$('#exampleModal').modal('show');
consultaCliente()
}

function consultaCliente() {
    // var url = $("#formProject").attr("data-project-url");
    var id = $("#identificacion").val();
	var host ="/consdavivienda/elementos/"+id+"/" 
	$.ajax({
	type: "GET",
	dataType: "json",
	url: host,
	complete: function(data) {
		console.log(data.responseJSON[0]['fields'].identificacion)
		$('#form_identificacion').val(data.responseJSON[0]['fields'].identificacion)
		$('#form_total_oper_pendientes').val(data.responseJSON[0]['fields'].total_oper_pendientes)
        $('#form_total_oper_liquidadas').val(data.responseJSON[0]['fields'].total_oper_liquidadas)
        $('#form_total_oper_anuladas').val(data.responseJSON[0]['fields'].total_oper_anuladas)
        $('#form_total_tran_eur').val(data.responseJSON[0]['fields'].total_tran_eur)
        $('#form_total_tran_usd').val(data.responseJSON[0]['fields'].total_tran_usd)
        $('#form_total_tran_cad').val(data.responseJSON[0]['fields'].total_tran_cad)
        $('#form_total_oper_v').val(data.responseJSON[0]['fields'].total_oper_v)
        $('#form_total_oper_c').val(data.responseJSON[0]['fields'].total_oper_c)
        $('#form_total_oper_j').val(data.responseJSON[0]['fields'].total_oper_j)
        $('#form_maxim_d_sin_oper').val(data.responseJSON[0]['fields'].maxim_d_sin_oper)

	}
	});

}

function consultaPerfil() { 
   var id = $("#identificacion").val();
   window.location = "/consdavivienda/tarjetaresumen/"+id;
}