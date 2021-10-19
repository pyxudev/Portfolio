<?php
$uuid = strval(uniqid());
$user_url = $_POST['user_url'];
$task_type = $_POST['task_type'];
$cols = $_POST['cols'];
$rows = $_POST['rows'];
$deadline = $_POST['deadline'];
$gap_date = $_POST['gap_date'];

#for test
// $user_url = 'https://google.com';
// $task_type = '定期的に収集';
//$cols = 123;
//$rows = 321;
// $deadline = '2021-02-10';
// $gap_date = 20;

$url = 'http://127.0.0.1:6800/schedule.json';

$data = array(
	'project' => 'speed_score',
	'spider' => 'speed_score',
	'user_url' => $user_url,
	'task_type' => $task_type,
	'cols' => $cols,
	'rows' => $rows,
	'deadline' => $deadline,
    'gap_date' => $gap_date,
    'uuid' => $uuid);

$context = array(
	'http' => array(
		'method'  => 'POST',
		'header'  => implode("\r\n", array('Content-Type: application/x-www-form-urlencoded')),
		'content' => http_build_query($data),
	),
);

$html = file_get_contents($url, false, stream_context_create($context));

ob_start();
passthru("/srv/www/public_html/speed_score/env/bin/python3 /srv/www/public_html/speed_score/speed_score/personal_notis.py ${cols} ${rows} ${deadline} ${task_type} ${user_url}");
echo $uuid;

exit;
?>
