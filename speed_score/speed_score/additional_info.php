<?php
$uuid = $_POST['uuid'];
$company_name = strval($_POST['company_name']);
$user_name = strval($_POST['user_name']);
$phone_number = strval($_POST['phone_number']);
$email = strval($_POST['email']);
$task_type = strval($_POST['task_type']);
$frequency = 'null';
$delivery = 'null';
$data_order= 'null';

$pdo = new PDO(
	'mysql:dbname=[name];host=[host];',
	'user_name',
	'pw'
);

$time = 0;
while ($time < 101) {
	sleep(1);
	if ($task_type == "一回きりの収集") {
		$sth = $pdo->prepare("SELECT * FROM speed_score WHERE uuid = :uuid");
	}
	else {
		$sth = $pdo->prepare("SELECT * FROM speed_score_periodical WHERE uuid = :uuid");
	}

	$sth->bindParam(':uuid', $uuid);
	$sth->execute();

	if ($sth -> rowCount()){
		$mysql = $pdo -> prepare('UPDATE :table SET company_name = :company_name, user_name = :user_name, phone_number = :phone_number, email = :email WHERE uuid = :uuid ;');
		$mysql->bindParam(':table', $table);
		$mysql->bindParam(':company_name', $company_name);
		$mysql->bindParam(':user_name', $user_name);
		$mysql->bindParam(':phone_number', $phone_number);
		$mysql->bindParam(':email', $email);
		$mysql->bindParam(':uuid', $uuid);
		$mysql->execute();

		foreach($sth as $line) {
			$id = strval($line['id']);
			$result = strval($line['result']);
			$cols = strval($line['cols']);
			$rows = strval($line['rows']);
			$user_url = strval($line['user_url']);
			$deadline = strval($line['deadline']);
		}
		$file_path = "/srv/www/public_html/speed_score/env/bin/python3 /srv/www/public_html/speed_score/speed_score/"
		$info = "${company_name} ${result} ${id} ${task_type} ${cols} ${rows}"

		ob_start();
		passthru($file_path + "pdf_generate.py" + $info + "${deadline} ${user_url}");
		passthru($file_path + "slack_notis.py " + $info + "'${frequency}' '${delivery}' '${data_order}' ${deadline} ${task_type} ${user_url}");
		echo $id;
		break;
	}
	else {
		$time++;
	}
}

exit;
?>