
$(window).on('load', function(){
	$('#loader').fadeOut();
	$('#preloader').delay(3000).fadeOut('slow');
});

$(document).ready(function(){
	$('#filings').DataTable({
		
		// "searching": false,
		'pageLength' : 25,
		'autoWidth' : true,
		'scrollY' : "40vh"
	});


	$('.btn_back').on('click', function(){
		
		$("#back_form").submit();
	});

	
	$('.btn_next').on('click', function(){
		$('#confirm').show();
	});

	$('.yes').on('click', function(){

		var cr_no = $('#cr_no').val();
		$.ajax({
			url: '/intermediate',
			data: $('form').serialize(),
			type: "POST",
			success: function(response){
				console.log(response);
				if ((response == "Insufficient") || (response == "Network")) {
					$('#confirm').hide();
				}
				else{
					var obj = $.parseJSON(response);
					var result = obj['result'];
					
					$('#address').val(result['address']);
					$('#capital').val(result['capital']);
					$('#secretary').val(result['secretary']);
					$('#receiver').val(result['receiver']);
					$('#liquidator').val(result['liquidator']);

					var list_of_directors = result['directors'];
					for (var i = 0; i < list_of_directors.length; i++) {
						$('#directors').append('<tr><td>'+list_of_directors[i]['no']+'</td><td>'+list_of_directors[i]['name']+'</td></tr>');
					}

					$('#btn_basic').removeClass('btn-primary');
					$('#btn_basic').addClass('btn-success');
					$('#btn_basic').val('Complete');

					$('#btn_intermediate').removeClass('btn-secondary');
					$('#btn_intermediate').addClass('btn-primary');
					$('#btn_intermediate').val('In Progress');

					$('#confirm').hide();
					$('#intermediate_result').show();
				}
			},
			error: function(error){
				console.log(error);
			}

		});		

	});

	$('.no').on('click', function(){
		$('#confirm').hide();
	});

	$('#btn_intermediate').on('click', function(){
		$('#confirm').show();
	});

});