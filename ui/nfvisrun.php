<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>NFVIS Deployment</title>
    <style>
            P {text-align: center; }
            IMG {text-align: center; }
            Form {text-align: center; }
	        p { font-family: "Arial", "Times", "serif"; }
            p.main { font-size: 120% }
     </style>
</head>
<body>
    <br>
    <p><strong>While we're turning up the FW at the branch, take a look at your Spark room for messages</p>
    <p><a href="gadd-h100.html"><IMG SRC="images/nfvisrun_opt.png"></a></p>
    <?php exec("python ../nvfis_app.py"); ?>
</body>
</html>
