<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>

    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>Gadd NFVis ACI</title>
        <link rel="shortcut icon" href="images/favicon.ico" type="image/x-icon" />

        <style>
            P {text-align: center; }
            IMG {text-align: center; }
            Form {text-align: center; }
	        p { font-family: "Arial", "Times", "serif"; }
            p.main { font-size: 120% }
        </style>
        <script src="amcharts/amcharts.js" type="text/javascript"></script>
        <script src="amcharts/gauge.js" type="text/javascript"></script>
        <script> var H = <?php require('aciprerun.php'); ?></script>
        <script>
            var ACI_H = H // Set ACI health score value here
            var health = ACI_H; 
            var chart = AmCharts.makeChart("chartdiv", {
                type: "gauge",
                titles: [{
                    "text": "Gadd Application Health (ACI)",
                    "size": 20
                }],

                axes: [{
                    startValue: 0,
                    axisThickness: 2,
                    endValue: 100,
                    valueInterval: 10,
                    bottomTextYOffset: -20,
                    bottomText: "Health Score",

                    bands: [{
                            startValue: 0,
                            endValue: 45,
                            innerRadius: "70%",
                            color: "#ea3838"
                        },

                        {
                            startValue: 45,
                            endValue: 80,
                            innerRadius: "70%",
                            color: "#ffac29"
                        },

                        {
                            startValue: 80,
                            endValue: 100,
                            innerRadius: "70%",
                            color: "#00CC00",
                        }
                    ]
                }],

                arrows: [{}]
            });

            setInterval(randomValue, 1000);
            
             // set random value
            function randomValue() {
                var value = Math.round(Math.random() * 0.5 + health);
                //var value = value; // set this value from ACI
                chart.arrows[0].setValue(value);
                chart.axes[0].setBottomText("Health Score");
            }
        </script>
    </head>

    <body>
        <hr size=50 noshade color="#006699"></hr>
        <br>
        <div id="chartdiv" style="width:800px; height:400px; margin:0 auto;"></div>

        <p class="main"><strong>
        Cisco NGIPS detected a threat to Gadd Application from remote branch!<br></p>
        <p><a href="nfvisrun2.php"><IMG SRC="images/virus_opt.png" alt="virus"></a></p>

    </body>

</html>
