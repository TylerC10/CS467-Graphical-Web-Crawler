<html>
    <head>
        <title>PHP Database Connect</title>
        <link rel="stylesheet" href="styles.css">
        <link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Allerta" />
    </head>
     <body>
         <?php ini_set('display_errors', 1); ?>
        <?php
         header('Content-type: application/json; charset=utf-8');
         $db_connection = pg_connect("host = firstdbinstance.cxvcjdies8vv.us-east-2.rds.amazonaws.com dbname = beginning_database user = copety  password = eridanus port = 5432");
     ?>
</html>
