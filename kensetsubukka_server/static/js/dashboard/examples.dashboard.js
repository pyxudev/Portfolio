$(window).on('load',function() {
	$('.sidebar-toggle').click();
	fadeout();
});

function call_request_scraping(){
	var request_1 = document.getElementsByClassName('request_type1');
	var request_2 = document.getElementsByClassName('request_type2');
	var message = "よろしいですか？";
	// console.log(message);
	var message_2 = "進行中のリクエストがあります。 新しいリクエストを開始すると、進行中のリクエストはキャンセルされます。 そうしますか？"
	if (request_1[0] != null || request_2[0] !=null){
		if (confirm(message_2)) {
			$.ajax({
				url: "/dashboard/new_request/",
				method: "POST",
				success: function(response){
					$('.request-body').html(response);
				},
			});
		}
	}
	else{
		$.ajax({
			url: "/dashboard/new_request/",
			method: "POST",
			success: function(response){
				$('.request-body').html(response);
			},
		});
	}
	fadeout();
}


function refresh_requests(){
	window.location.reload();
}


function cancel_request(Task_Id){
	$.ajax({
		url: "/dashboard/cancel_request/",
		method: "POST",
		data: {"task_id":Task_Id},
		success: function(response){
			$('.request-body').html(response);
		},
	});
	fadeout();
}

function download_file(Task_Id){
	$.ajax({
		url: "/dashboard/download/",
		method: "GET",
		data: {"task_id":Task_Id},
		
		success: function(response,status,xhr){
			filename = xhr.getResponseHeader('Content-Disposition').split("filename=")[1];
			var blob=new Blob([response]);
			var link=document.createElement('a');
			link.href=window.URL.createObjectURL(blob);
			link.download=filename;
			link.click();
		},
	});
}


function fadeout(){
	setTimeout(function(){
		$('.request_type3').fadeOut();
		$('.request_type5').fadeOut();
		$('.request_type6').fadeOut();
		$.ajax({
			url: "/dashboard/update_status/",
			method: "POST",
			success: function(response){
				console.log("Database Updated.")
			},
		});
	},5000)
}

$(function () {
	$('[data-toggle="tooltip"]').tooltip()
})

function off() {
	document.getElementById("content").style.filter = "blur(0px)";
	document.getElementById("overlay").style.display = "none";
}

function see_logs() {
	off();
	document.getElementById("content").style.filter = "blur(4px)";
	$.ajax({
		url: "/dashboard/see_logs/",
		method: "GET",
		success: function(response){
			$('#overlay').html(response);
			document.getElementById("overlay").style.display = "block";
		},
	});
	fadeout();
}

function change_password() {
	off();
	document.getElementById("content").style.filter = "blur(4px)";
	$.ajax({
		url: "/dashboard/change_password/",
		method: "GET",
		success: function(response){
			$('#overlay').html(response);
			document.getElementById("overlay").style.display = "block";
		},
	});
	fadeout();
}

function update_password() {
	$.ajax({
		url: "/dashboard/change_password/",
		method: "POST",
		data: $('#change_password').serialize(),
		success: function(response){
			$('#overlay').html(response);
			document.getElementById("overlay").style.display = "block";
		},
	});
	return false;
}
