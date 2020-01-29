// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';
// Pie Chart Example
consultaDivisas()
function consultaDivisas() {
    // var url = $("#formProject").attr("data-project-url");
	var result =[];
	var host ="http://127.0.0.1:8000/consdavivienda/totaldivisas/1/" 
	$.ajax({
	type: "GET",
	dataType: "json",
	url: host,
	complete: function(data) {
	   console.log(data.responseJSON.total_usd)
	   //alert(data.responseJSON[0]['fields'].total_usd)
	   result=[data.responseJSON.total_usd,data.responseJSON.total_eur,data.responseJSON.total_cad];
	   console.log(result);
	   pintarPie(result)
	   
	}
	});
}



function pintarPie(array_data) { 
	var ctx = document.getElementById("myPieChart");
	var myPieChart = new Chart(ctx, {
	  type: 'pie',
	  data: {
		labels: ["Usd", "Eur", "Cad"],
		datasets: [{
		  data: array_data,
		  backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'],
		}],
	  },
	});
}

pintarPie() ;
