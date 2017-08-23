<html>
    <head>
        <title>PHP Form Test</title>
        <link rel="stylesheet" href="styles.css">
        <link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Allerta" />
    </head>
    <body>
        <?php

        $search_type = $_POST['search_type'];
        $start_url = $_POST['start_url'];
        $stop_words = $_POST['stop_words'];
        echo $search_type;
        echo $start_url;
        echo $stop_words;
        
        ?>
    </body>
</html>
