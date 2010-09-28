<?php

function err()
{
    header('Location: error.html');
    exit;
}

function makesafe($txt)
{
    $alpha = 'abcdefghijklmnopqrstuvwxyz';
    $ret = array();
    for ($i = 0; $i < strlen($txt); $i++)
        if (false !== strpos($alpha, $txt[$i])) $ret[] = $txt[$i];

    return join($ret, '');
}

if (!isset($_FILES['po']) or
    ($_FILES['po']['error'] != 0) or
    ($_POST['src_lang'] == '') or
    ($_POST['dest_lang'] == ''))
        err();

$src_lang = makesafe($_POST['src_lang']);
$dest_lang = makesafe($_POST['dest_lang']);

$src_fname = $_FILES['po']['tmp_name'];
$dest_fname = 'output/' . md5_file($src_fname) . '.po';

$cmd = 'python googtext.py ' . $src_fname . ' ' . $src_lang .
    ' ' . $dest_fname . ' ' . $dest_lang;

exec($cmd, &$output, &$retval);

if ($retval != 0)
    err();

header('Location: ' . $dest_fname);

?>
