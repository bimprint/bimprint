<?php

// Retrieve ID
$id = htmlspecialchars($_GET["id"]);

// Execute command
$command = '/bimprint/install/python-3.4.2/bin/python3 /srv/bimprint/main.py ' . $id . ' > /var/www/html/files/plan-' . $id . '.svg';
shell_exec($command);

// Download file
$file_url = 'http://www.bimprint.com/files/plan-' .$id. '.svg';
header('Content-Type: application/octet-stream');
header("Content-Transfer-Encoding: Binary"); 
header("Content-disposition: attachment; filename=\"" . basename($file_url) . "\""); 
readfile($file_url);

?>