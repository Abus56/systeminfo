<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
     var $email = $_POST["mail"];
     exec ("get_system_info.py $email &")
}

?>

<html>
    <head>
        <title> Отправка информации о системе </title>
    </head>
    <body>
        <div>
            <form method="POST" action="index.php">
                <label> введите email:<label>
                <input type="email" name="mail"/>
                <input type="submit">
            </form>

        <div>
    </body>
</html>
