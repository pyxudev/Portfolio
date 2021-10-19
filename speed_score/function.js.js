$(function() {
    fade('.toggleWrap');
    var button_1 = document.getElementsByClassName("open_btn");
    var fin_check = document.getElementsByClassName("fin_check");
    var button_2 = document.getElementsByClassName("redirect");
    var button_3 = document.getElementsByClassName("dowload_estimation");
    var animation = document.getElementById("estimating");
	var fin_check_detail = document.getElementsByClassName("fin_check_detail");
	var quick_estimate = document.getElementsByClassName("start_dev");
	var btn_2 = document.getElementsByClassName("btn-2");
	var change_html = document.getElementsByClassName("change-html");
	
	function sleep(waitSec, callbackFunc) {
		// 経過時間（秒）
		var spanedSec = 0;
		// 1秒間隔で無名関数を実行
		var id = setInterval(function () {
			spanedSec++;
			// 経過時間 >= 待機時間の場合、待機終了。
			if (spanedSec >= waitSec) {
				// タイマー停止
				clearInterval(id);
				// 完了時、コールバック関数を実行
				if (callbackFunc) callbackFunc();
			}
		}, 1000);
	}
	
	if (btn_2.length > 0) {
		btn_2[0].addEventListener("click",function open_link(){
			var link = btn_2[0].getAttribute("href");
			window.location.replace(link);
		});
		btn_2[1].addEventListener("click",function open_link_2(){
			var link_1 = btn_2[1].getAttribute("href");
			window.location.replace(link_1);
		});
	}

    if (button_1.length > 0) {
        button_1[0].addEventListener("click", function send_url() {
			var user_url = document.getElementsByName("collect_url")[0].value;
			var v_2 = document.getElementsByName("data_col")[0].value;
			var v_3 = document.getElementsByName("data_row")[0].value;
			var task_type = 0;
			var type_1 = document.getElementById("pills-home-tab");
			var type_2 = document.getElementById("pills-profile-tab");
			var activate_1 = type_1.getAttribute("aria-selected");
			var activate_2 = type_2.getAttribute("aria-selected");
			var v_4 = document.getElementsByName("time")[0].value;
			var v_year = v_4.substring(0, 4);
			var v_month = v_4.substring(5, 7);
			var v_date = v_4.substring(8, 10);
			var entered_date = new Date(v_year, v_month, v_date);
			var date = new Date();
			var gap_date = (entered_date - date) / 86400000 - 29;
			
			var sele_frc = [];
			var sele_delv = [];
			var sele_order = [];
			var option = 0;
			var option_frc = 0;
			var option_delv = 0;
			var option_order = 0;
					
			if (activate_1 == "true") {
				task_type = type_1.getAttribute("value");
				document.getElementsByName("collect_type")[0].value = task_type;
			} else if (activate_2 == "true") {
				task_type = type_2.getAttribute("value");
				document.getElementsByName("collect_type")[0].value = task_type;
				var frequncy_1 = document.getElementById("regular-label");
				if (frequncy_1){
					var frequncy_2 = document.getElementById("apibase-label");
					var frequncy_3 = document.getElementById("click-label");

					var delivery_1 = document.getElementById("api-label");
					var delivery_2 = document.getElementById("mail-label");
					var delivery_3 = document.getElementById("file-exist-label");
					var delivery_4 = document.getElementById("file-new-label");
					var delivery_5 = document.getElementById("db-exist-label");
					var delivery_6 = document.getElementById("db-new-label");
					var delivery_7 = document.getElementById("download-label");

					var order_1 = document.getElementById("data-managed-label");
					var order_2 = document.getElementById("data-gap-label");
					var order_3 = document.getElementById("alert-mail-label");
					var order_4 = document.getElementById("save-data-label");
					var order_5 = document.getElementById("has-error-label");

					var frc_arry = [frequncy_1, frequncy_2, frequncy_3];
					var delv_arry = [delivery_1, delivery_2, delivery_3, delivery_4, delivery_5, delivery_6, delivery_7];
					var order_arry = [order_1, order_2, order_3, order_4];
					
					for (const frc_elem of frc_arry){
						if (frc_elem.checked){
							sele_frc.push(frc_elem.getAttribute("value"));
							if(frc_elem.getAttribute("value") == "定期収集"){
								option_frc = option_frc + 3;
							}
							else if(frc_elem.getAttribute("value") == "収集API"){
								option_frc = option_frc + 15;
							}
							else if(frc_elem.getAttribute("value") == "専用Web"){
								option_frc = option_frc + 6;
							}
						}
					}
					
					for (const delv_elem of delv_arry){
						if (delv_elem.checked){
							sele_delv.push(delv_elem.getAttribute("value"));
							if(delv_elem.getAttribute("value") == "送信API"){
								option_delv = option_delv + 9;
							}
							else if(delv_elem.getAttribute("value") == "メール自動送信"){
								option_delv = option_delv + 6;
							}
							else if(delv_elem.getAttribute("value") == "ファイルサーバー(既存)"){
								option_delv = option_delv + 6;
							}
							else if(delv_elem.getAttribute("value") == "ファイルサーバー(構築)"){
								option_delv = option_delv + 9;
							}
							else if(delv_elem.getAttribute("value") == "DB格納(御社準備)"){
								option_delv = option_delv + 6;
							}
							else if(delv_elem.getAttribute("value") == "DB格納(弊社準備)"){
								option_delv = option_delv + 9;
							}
							else if(delv_elem.getAttribute("value") == "Web上DL"){
								option_delv = option_delv + 6;
							}
						}
					}
					
					for (const order_elem of order_arry){
						if (order_elem.checked){
							sele_order.push(order_elem.getAttribute("value"));
							if(order_elem.getAttribute("value") == "データの増減チェック"){
								option_order = option_order + 3;
							}
							else if(order_elem.getAttribute("value") == "データの更新チェック"){
								option_order = option_order + 6;
							}
							else if(order_elem.getAttribute("value") == "キーワード出現通知"){
								option_order = option_order + 6;
							}
							else if(order_elem.getAttribute("value") == "エラー通知(メール)"){
								option_order = option_order + 6;
							}
							else if(order_elem.getAttribute("value") == "エラー通知(slack)"){
								option_order = option_order + 6;
							}
						}
					}
					
					option = (option_frc + option_delv + option_order + 20)*10000;
					if (sele_frc.length > 0){
						sele_frc = sele_frc.join(',');
					}
					else {
						sele_frc = 0;
					}
					if (sele_delv.length > 0){
						sele_delv = sele_delv.join(',');
					}
					else {
						sele_delv = 0;
					}
					if (sele_order.length > 0){
						sele_order = sele_order.join(',');
					}
					else {
						sele_order = 0;
					}
				}
			}
			if (user_url.length > 0 && user_url.substr(0,4) === "http" && gap_date > 0 && v_2.length > 0 && Number.isInteger(Number(v_2)) && v_3.length > 0 && Number.isInteger(Number(v_3)) && v_2 > 0 && v_3 > 0) {
				document.getElementById("trigger").setAttribute("type","checkbox");
				document.getElementById('estimate-1').classList.remove("estimated");
				scrollTo(0, 0);

				if(location.href == "https://services.sms-datatech.co.jp/pig-data/webestimation/"){
					$.ajax({
						type: "POST",
						url: "/speed_score/speed_score/pass_url.php",
						data: {
							user_url : user_url,
							task_type : task_type,
							rows : v_2,
							cols : v_3,
							deadline : v_4,
							gap_date : gap_date
						},
						success: function(data) {
							var uuid = data;

							localStorage.setItem('uuid', uuid);
							localStorage.setItem("task_type", task_type);
							console.log("Done");
						},
						error: function() {
							location.href='https://services.sms-datatech.co.jp/pig-data/estimation_error/';
						}
					});
				}
				else{
					console.log(sele_frc);
					console.log(sele_delv);
					console.log(sele_order);
					console.log(option);
					
					$.ajax({
						type: "POST",
						url: "/speed_score/speed_score/int-dev.php",
						data: {
							user_url : user_url,
							task_type : task_type,
							rows : v_2,
							cols : v_3,
							deadline : v_4,
							gap_date : gap_date,
							option_frc : option_frc,
							option_delv : option_delv,
							option_order : option_order,
							frcs : sele_frc,
							delv : sele_delv,
							orders : sele_order,
							option : option
						},
						success: function(data) {
							var uuid = data;

							localStorage.setItem('uuid', uuid);
							localStorage.setItem("task_type", task_type);
							console.log("Done, here");
						}
					});
				}
				sleep(15, function () {
					document.getElementById('estimate-1').classList.add('estimated');
					var popup = document.getElementsByClassName("popup_content")[0];
					popup.classList.remove("estimated");
				});
			} else {
				if (user_url.length < 1 || user_url.substr(0,4) != "http"){
					document.getElementById('alert_url').innerHTML = "収集したいURLを入力してください。"
				}
				if (user_url.length > 0 && user_url.substr(0,4) === "http"){
					document.getElementById('alert_url').innerHTML = ""
				}
				if (v_2.length < 1 || !Number.isInteger(Number(v_2)) || v_2 < 1) {
					document.getElementById('alert_col').innerHTML = "正しい数値を入力してください。";
				} else {
					document.getElementById('alert_col').innerHTML = "";
				}
				if (v_3.length < 1 || !Number.isInteger(Number(v_3)) || v_3 < 1) {
					document.getElementById('alert_row').innerHTML = "正しい数値を入力してください。";
				} else {
					document.getElementById('alert_row').innerHTML = "";
				}
				if (gap_date === 0) {
					document.getElementById('alert_date').innerHTML = "納期を本日に選択することはできません。";
				} else if (gap_date < 0) {
					document.getElementById('alert_date').innerHTML = "納期に本日よりも前の日付が入力されています。";
				} else {
					document.getElementById('alert_date').innerHTML = "";
				}
			}
		});
		var uuid = localStorage.getItem("uuid");
		localStorage.setItem('uuid', uuid);
	}
	
    if (fin_check.length > 0) {
        fin_check[0].addEventListener("click", function fine() {
			var company_name = document.getElementsByName("company")[0].value;
			var user_name = document.getElementsByName("name")[0].value;
			var phone_number = document.getElementsByName("number")[0].value.replace(/[━.*‐.*―.*－.*\-.*ー.*\-]/gi,'');
			var email = document.getElementsByName("email")[0].value;
			var reg = /^[A-Za-z0-9]{1}[A-Za-z0-9_.-]*@{1}[A-Za-z0-9_.-]{1,}\.[A-Za-z0-9]{1,}$/;
			var reg_1 = /^[A-Za-z0-9]{1}[A-Za-z0-9_.-]*@gmail.com$/;
			var reg_2 = /^[A-Za-z0-9]{1}[A-Za-z0-9_.-]*@i-cloud.com$/;
			var reg_3 = /^[A-Za-z0-9]{1}[A-Za-z0-9_.-]*@mail.yahoo.co.jp$/;
			var btn = document.getElementById("fin_btn");
			
			if (company_name.length > 0 && user_name.length > 0 && phone_number.length > 0 && email.length > 0 && phone_number.match(/^(0[5-9]0[0-9]{8}|0[1-9][1-9][0-9]{7})$/) && reg.test(email) && !reg_1.test(email) && !reg_2.test(email) && !reg_3.test(email)) {
				btn.classList.remove('estimated');
				document.getElementsByClassName("check_img")[0].src = "/pig-data/wp-content/uploads/checked.png";
				document.getElementsByClassName("fake_btn")[0].classList.add("estimated");
				document.getElementById('alert_comp').innerHTML = "";
				document.getElementById('alert_user').innerHTML = "";
				document.getElementById('alert_user').innerHTML = "";
				document.getElementById('alert_email').innerHTML = "";
				document.getElementById("satori__customer_lead_company_name").value = company_name;
				document.getElementById("satori__customer_last_name").value = "name";
				document.getElementById("satori__customer_first_name").value = user_name;
				document.getElementById("satori__customer_email").value = email;
				document.getElementById("satori__customer_phone_number").value = phone_number;
				document.getElementById("satori__privacy_policy_agreement").checked = true;
				document.getElementsByClassName("satori__btn submit satori__submit_confirm_5c26f253c5c39f32 satori__show")[0].click();
				
				localStorage.setItem('company_name', company_name);
				localStorage.setItem('user_name', user_name);
				localStorage.setItem('phone_number', phone_number);
				localStorage.setItem('email', email);
			} else {
				btn.classList.add('estimated');
				document.getElementsByClassName("fake_btn")[0].classList.remove("estimated");
				if (company_name.length < 1){
					document.getElementById('alert_comp').innerHTML = "お勤め先を入力してください。";
				} else if (company_name.length > 0){
					document.getElementById('alert_comp').innerHTML = "";
				}
				if (user_name.length < 1){
					document.getElementById('alert_user').innerHTML = "お客様の氏名を入力してください。";
				} else if (user_name.length > 0){
					document.getElementById('alert_user').innerHTML = "";
				}
				if (phone_number.length < 1 || !phone_number.match(/^(0[5-9]0[0-9]{8}|0[1-9][1-9][0-9]{7})$/)){
					document.getElementById('alert_phone').innerHTML = "正しい電話番号をを入力してください。";
				} else if (phone_number.length > 0 && phone_number.match(/^(0[5-9]0[0-9]{8}|0[1-9][1-9][0-9]{7})$/)){
					document.getElementById('alert_phone').innerHTML = "";
				}
				if (email.length < 1) {
					document.getElementById('alert_email').innerHTML = "メールアドレスが入力されていません。";
				} else if (email.length > 0) {
					document.getElementById('alert_email').innerHTML = "";
				}
				if (email.length > 0 && !reg.test(email) || reg_1.test(email) || reg_2.test(email) || reg_3.test(email)){
					document.getElementById('alert_email').innerHTML = "正しいメールアドレスを入力してください、プライベート用E-mailはご使用になれません。";
				}
			}
		});
    }
	
    if (animation) {
		var uuid = localStorage.getItem("uuid");
		var company_name = localStorage.getItem("company_name");
		var user_name = localStorage.getItem("user_name");
		var phone_number = localStorage.getItem("phone_number");
		var email = localStorage.getItem("email");
		var task_type = localStorage.getItem("task_type");

		document.getElementsByName("company_name")[0].value = company_name;
		document.getElementsByName("user_name")[0].value = user_name;
		document.getElementsByName("phone_number")[0].value = phone_number;
		document.getElementsByName("email")[0].value = email;
		
		if(location.href == "https://services.sms-datatech.co.jp/pig-data/estimate-contact/"){
			$.ajax({
				type: "POST",
				url: "/speed_score/speed_score/additional_info.php",
				data: {
					uuid : uuid,
					company_name : company_name,
					user_name : user_name,
					phone_number : phone_number,
					email : email,
					task_type : task_type
				},
				success: function(data) {
					var id = data;
					console.log(id);
					print_file();
				}
			});
		}
		else{
			$.ajax({
				type: "POST",
				url: "/speed_score/speed_score/out-dev.php",
				data: {
					uuid : uuid,
					company_name : company_name,
					user_name : user_name,
					phone_number : phone_number,
					email : email,
					task_type : task_type
				},
				success: function(data) {
					print_file();
				},
				error: function() {
					location.href='https://services.sms-datatech.co.jp/pig-data/estimation_error/';
				}
			});
		}
	}
	
	if (fin_check_detail.length > 0) {
        fin_check_detail[0].addEventListener("click", function fine_satori() {
			var detail = document.getElementsByName("ask")[0].value;
			var email = localStorage.getItem("email");
			var reg_1 = /^[A-Za-z0-9]{1}[A-Za-z0-9_.-]*@gmail.com$/;
			var reg_2 = /^[A-Za-z0-9]{1}[A-Za-z0-9_.-]*@i-cloud.com$/;
			var reg_3 = /^[A-Za-z0-9]{1}[A-Za-z0-9_.-]*@mail.yahoo.co.jp$/;
			
			if (!reg_1.test(email) && !reg_2.test(email) && !reg_3.test(email)) {
				document.getElementById("satori__customer_email").value = email;
				document.getElementById("satori__custom_field_3589acd614807d298").value = detail;
				document.getElementById("satori__privacy_policy_agreement").checked = true;
				document.getElementsByClassName("satori__btn submit satori__submit_confirm_fd4fc9b850bb92e5 satori__show")[0].click();
				document.getElementsByClassName("check_img")[0].src = "/pig-data/wp-content/uploads/checked.png";
			}
		});
	}

	function print_file(){
		var company_name = localStorage.getItem("company_name");
		var task_type = localStorage.getItem("task_type");
		var file_name = "/speed_score/speed_score/見積書_" + company_name + "様_" + task_type + ".pdf";
		document.getElementById("estimate_pdf").src = file_name;
		localStorage.setItem('file_name', file_name);
		const spinner = document.getElementById('estimating');
		spinner.classList.add('estimated');
	}
	
    if (button_2.length > 0) {
        button_2[0].addEventListener("click", function redirect(){
			window.location.replace("https://services.sms-datatech.co.jp/pig-data/webestimation");
		});
    }
	
    if (button_3.length > 0) {
        button_3[0].addEventListener("click", function dowload_estimation(){
			var file_name = localStorage.getItem("file_name");
			location.href = file_name;
		});
    }
	
	if (quick_estimate.length > 0) {
		load_logs();
        quick_estimate[0].addEventListener("click", function quick_estimate(){
 			document.getElementById("load_img").setAttribute("src"," /pig-data/wp-content/uploads/loading-dev.gif");
			scrollTo(0, 0);
			var user_url = document.getElementsByName("collect_url")[0].value;
			var task_name = document.getElementsByName("task_name")[0].value;
			var v_2 = document.getElementsByName("data_col")[0].value;
			var v_3 = document.getElementsByName("data_row")[0].value;
			var v_4 = document.getElementsByName("deadline")[0].value;
			var v_year = v_4.substring(0, 4);
			var v_month = v_4.substring(5, 7);
			var v_date = v_4.substring(8, 10);
			var entered_date = new Date(v_year, v_month, v_date);
			var date = new Date();
			var deadline = (entered_date - date) / 86400000 - 29;
			
			$.ajax({
				type: "POST",
				url: "/speed_score/speed_score/estimate_dev.php",
				data: {
					user_url : user_url,
					task_name : task_name,
					rows : v_2,
					cols : v_3,
					deadline : deadline
				},
				success: function(data) {
					var result_dev = data;
					localStorage.setItem('result_dev', result_dev);
					show_result();
				}
			});
		});
    }
	
	function load_logs(){
		$.ajax({
			type: "POST",
			url: "/speed_score/speed_score/read_logs.php",
			success: function(data) {
				var log = JSON.parse(data);
				var date = log.date;
				var name = log.name;
				var result = log.result;

				for (let i = 0; i < 5; i++){
					document.getElementsByClassName("date")[i].innerHTML = date[i];
					document.getElementsByClassName("name")[i].innerHTML = name[i];
					document.getElementsByClassName("result")[i].innerHTML = result[i];
				}
			}
		});	
	}
	
	function show_result(){
		console.log("Done");
		var result_dev = localStorage.getItem("result_dev");
		document.getElementById("result_showing").innerHTML = result_dev;
	}
	
	if (change_html.length > 0) {
		$.ajax({
			url: '/speed_score/speed_score/change_check.php',
			type: 'post'
		}).done(function(data){
			var status = document.getElementById('status');
			var new_element = document.createElement('p');
			
			if(data=="running"){
				console.log('busy');
				new_element.textContent = "状態：作動中、少々お待ちください。";
				status.appendChild(new_element);
				document.getElementsByClassName("status-check")[0].classList.add("invisible");
			}else{
				console.log('free');
				new_element.textContent = "状態：現在ご利用になれます";
				status.appendChild(new_element);
				document.getElementsByClassName("status-check")[0].classList.remove("invisible");
			}
		}).fail(function(){
			console.log('error');
		});
		
        change_html[0].addEventListener("click", function change_html() {
			var page_type = document.getElementById("page_type").value;
			var wrong = document.getElementById("wrong").value;
			var right = document.getElementById("right").value;
			
			$.ajax({
				url: '/speed_score/speed_score/change_html.php',
				type: 'post',
				data: {	
					page_type: page_type,
					wrong: wrong,
					right: right
				}
			}).done(function(data){
				console.log(data);
				document.getElementsByClassName("change-html")[0].classList.add("invisible");
			}).fail(function(){
				console.log('failed');
			});
		});
	}
	
    function fade(elm) {
        var $fade = $(elm),
            $body = $('body');
        // .toggleWrapを非表示にしておく
        $fade.addClass('hide');

        // #toggleがクリックされた時に、.hideの付け外しで .toggleWrapの表示・非表示を切り替え
        // .addClass('animation');でアニメーションのCSSを適応
        $('#toggle').on('click', function() {
            $fade.toggleClass('hide').addClass('animation');
            $('.trigger').toggleClass('active');

            // スクロールの制御
            // .hideを持っている状態はメニューが閉じている状態で、このときは.no-scrollは不要
            if ($fade.hasClass('hide')) {
                $body.removeClass('no-scroll').off('.noScroll');
            } else {
                // メニューが開いている時に、bodyに.no-scrollを追加してスクロールさせない
                $body.addClass('no-scroll').on('touchmove.noScroll', function(e) {
                    e.preventDefault();
                });
            }
        });
    }
});