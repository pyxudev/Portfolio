<?php
$uuid = strval($_POST['uuid']);
$option_frc = strval($_POST['option_frc']);
$option_delv = strval($_POST['option_delv']);
$option_order = strval($_POST['option_order']);
$frcs = strval($_POST['frcs']);
$delv = strval($_POST['delv']);
$data_order = strval($_POST['data_order']);
$options = strval($_POST['options']);

// $uuid = '60c95ac302641';
// $frcs = '専用Web';
// $delv = 'メール自動送信,DB格納(御社準備),Web上DL';
// $orders = 'データの増減チェック';
// $option_frc = "10000";
// $option_delv = "20000";
// $option_order =  "30000";
// $options = "100000";

$pdo = new PDO(
	'mysql:dbname=pigdata_extra;host=rds-aurora-cluster.cluster-cw2qkc1hesa1.ap-southeast-2.rds.amazonaws.com;charset=utf8;',
	'pigdata_extra',
	'pig0831'
);

$time = 0;
while ($time < 101) {
	sleep(1);
	$pre_mysql = 'SELECT * FROM speed_score_periodical WHERE uuid = :uuid;';
	$stmt = $pdo -> prepare($pre_mysql);
	$stmt -> bindParam(':uuid', $uuid);
	$stmt->execute();

	if ($stmt->rowCount()){
		$mysql = 'UPDATE speed_score_periodical SET frequency = :frcs, delivery = :delv, data_order = :data_order, options = :options, result = result, option_frc = :option_frc, option_delv = :option_delv, option_order = :option_order, done = 1 WHERE uuid = :uuid';

		$stmt = $pdo -> prepare($mysql);
		$stmt -> bindParam(':option_frc', $option_frc, PDO::PARAM_STR);
		$stmt -> bindParam(':option_delv', $option_delv, PDO::PARAM_STR);
		$stmt -> bindParam(':option_order', $option_order, PDO::PARAM_STR);
		$stmt -> bindParam(':frcs', $frcs, PDO::PARAM_STR);
		$stmt -> bindParam(':delv', $delv, PDO::PARAM_STR);
		$stmt -> bindParam(':data_order', $data_order, PDO::PARAM_STR);
		$stmt -> bindParam(':options', $options, PDO::PARAM_STR);
		$stmt -> bindParam(':uuid', $uuid);
		$stmt->execute();
		break;
	}
	else {
		$time++;
	}
}
exit;
?>