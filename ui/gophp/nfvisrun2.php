<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>NFVIS Deployment</title>
    <link rel="shortcut icon" href="images/favicon.ico" type="image/x-icon" />
    <style>
            P { text-align: center; }
	        p { font-family: "Arial", "Times", "serif"; }
            p.main { font-size: 130% }
     </style>
</head>
<body>
    <br>
    <br>
    <br>
    <br>
    <br>
    <h3><p class="main">While we're turning up the ASA at the branch,<br>
    please take a look at your Spark room for messages.</p></h3>
    <br>
    <br>
    <p><a href="gadd-h100-2.php"><IMG SRC="images/globe.png" alt="globe icon"></a></p>
    <script><?php exec("python ../../nfv_app.py"); ?></script>
</body>
</html>
