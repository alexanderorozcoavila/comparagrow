<?php 
    $link = mysqli_connect("localhost", "administrador", "BtCFfa~G5n=9", "instacandanga");
    
    if ($link == false) {
        die("ERROR: Could not connect. "
                    .mysqli_connect_error());
    }

    $sql = "SET NAMES 'utf8'";
    mysqli_query($link, $sql);
    $sql = "SELECT * FROM gs_sitios";
    if ($res = mysqli_query($link, $sql)) {
        if (mysqli_num_rows($res) > 0) {
            while ($row = mysqli_fetch_array($res)) {
                echo '[*] >> ' . $row['url'] . ': ';
                if (ValidarUrl($row['url']))
                    echo "Dirección existente \n";
                else
                    echo "Dirección inexistente \n";
            }
        }
    }

    function ValidarUrl($url) {
        $validar = @fsockopen($url, 80, $errno, $errstr, 15);
        if ($validar) {
         fclose($validar);
         return true;
        }else
         return false;
    }
?>