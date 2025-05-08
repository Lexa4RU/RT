<!DOCTYPE html>
<html>
<head>
<script type="text/javascript">
window.onload = function () {
    var chart = new CanvasJS.Chart("chartContainer");

    // chart.options.axisY = { prefix: "~", suffix: "M" };
    chart.options.title = { text: "Fruits sold in First & Second Quarter" };

    var series1 = { //dataSeries - first quarter
        type: "column",
        name: "First Quarter",
        showInLegend: true
    };

    var series2 = { //dataSeries - second quarter
        type: "column",
        name: "Second Quarter",
        showInLegend: true
    };

    var series3 = { //dataSeries - third quarter
        type: "column",
        name: "ThirdQuarter",
        showInLengend: true
    }

    var series4 = { //dataSeries - Fourth quarter
        type: "column",
        name: "FourthQuarter",
        showInLengend: true
    }

    chart.options.data = [];
    chart.options.data.push(series1);
    chart.options.data.push(series2);
    chart.options.data.push(series3);
    chart.options.data.push(series4);


    series1.dataPoints = [
		{ "label": "(07)", "y": 7281 },
		{ "label": "(76)", "y": 4359174 },
		{ "label": "(28)", "y": 2180460 },
		{ "label": "(08)", "y": 32225 },
		{ "label": "(52)", "y": 2485198 },
		{ "label": "(75)", "y": 4313188 },
		{ "label": "(94)", "y": 308238 },
		{ "label": "(84)", "y": 5527769 },
		{ "label": "(93)", "y": 3728166 },
		{ "label": "(27)", "y": 1895063 },
		{ "label": "(03)", "y": 111369 },
		{ "label": "(04)", "y": 492714 },
		{ "label": "(02)", "y": 290327 },
		{ "label": "(11)", "y": 7057926 },
		{ "label": "(32)", "y": 3330614 },
		{ "label": "(24)", "y": 1680603 },
		{ "label": "(44)", "y": 3466450 },
		{ "label": "(01)", "y": 322250 },
		{ "label": "(06)", "y": 41136 },
		{ "label": "(53)", "y": 2383440 }

    ];
    
    series2.dataPoints = [
		{ "label": "(07)", "y": 7281 },
		{ "label": "(76)", "y": 4359173 },
		{ "label": "(28)", "y": 2180455 },
		{ "label": "(08)", "y": 32211 },
		{ "label": "(52)", "y": 2485198 },
		{ "label": "(75)", "y": 4313188 },
		{ "label": "(94)", "y": 308230 },
		{ "label": "(84)", "y": 5527769 },
		{ "label": "(93)", "y": 3728161 },
		{ "label": "(27)", "y": 1895063 },
		{ "label": "(03)", "y": 111361 },
		{ "label": "(04)", "y": 492714 },
		{ "label": "(02)", "y": 290192 },
		{ "label": "(11)", "y": 7057905 },
		{ "label": "(32)", "y": 3330614 },
		{ "label": "(24)", "y": 1680603 },
		{ "label": "(44)", "y": 3466439 },
		{ "label": "(01)", "y": 322222 },
		{ "label": "(06)", "y": 41134 },
		{ "label": "(53)", "y": 2383425 }
    ];

    series3.dataPoints = [
        { "label": "(07)", "y": 7281 },
		{ "label": "(76)", "y": 4359173 },
		{ "label": "(28)", "y": 2180452 },
		{ "label": "(08)", "y": 32040 },
		{ "label": "(52)", "y": 2485198 },
		{ "label": "(75)", "y": 4313186 },
		{ "label": "(94)", "y": 308229 },
		{ "label": "(84)", "y": 5527764 },
		{ "label": "(93)", "y": 3727344 },
		{ "label": "(27)", "y": 1895063 },
		{ "label": "(03)", "y": 111361 },
		{ "label": "(04)", "y": 492714 },
		{ "label": "(02)", "y": 290090 },
		{ "label": "(11)", "y": 7057825 },
		{ "label": "(32)", "y": 3330614 },
		{ "label": "(24)", "y": 1680603 },
		{ "label": "(44)", "y": 3466438 },
		{ "label": "(01)", "y": 322210 },
		{ "label": "(06)", "y": 41134 },
		{ "label": "(53)", "y": 2383409 }

    ]

    series4.dataPoints = [
        { "label": "(07)", "y": 3776 },
		{ "label": "(76)", "y": 3687116 },
		{ "label": "(28)", "y": 1722157 },
		{ "label": "(08)", "y": 13114 },
		{ "label": "(52)", "y": 2057957 },
		{ "label": "(75)", "y": 3263848 },
		{ "label": "(94)", "y": 214369 },
		{ "label": "(84)", "y": 4039983 },
		{ "label": "(93)", "y": 3132384 },
		{ "label": "(27)", "y": 1430824 },
		{ "label": "(03)", "y": 57413 },
		{ "label": "(04)", "y": 454218 },
		{ "label": "(02)", "y": 156479 },
		{ "label": "(11)", "y": 6725551 },
		{ "label": "(32)", "y": 3099783 },
		{ "label": "(24)", "y": 1440479 },
		{ "label": "(44)", "y": 3168366 },
		{ "label": "(01)", "y": 206246 },
		{ "label": "(06)", "y": 0 },
		{ "label": "(53)", "y": 1262795 }

    ]

    chart.render();
}
</script>
<script type="text/javascript" src="https://cdn.canvasjs.com/canvasjs.min.js"></script>
</head>

<body>
    <div id="chartContainer" style="height: 300px; width: 100%;">
    </div>

    <p>
        <ul>
           <li>Saint-Barthélemy (07)</li>
           <li>Occitanie (76)</li>
           <li>Normandie (28)</li>
           <li>Saint-Martin (08)</li>
           <li>Pays de la Loire (52)</li>
           <li>Nouvelle-Aquitaine (75)</li>
           <li>Corse (94)</li>
           <li>Auvergne-Rhône-Alpes (84)</li>
           <li>Provence-Alpes-Côte d'Azur (93)</li>
           <li>Bourgogne-Franche-Comté (27)</li>
           <li>Guyane (03)</li>
           <li>La Réunion (04)</li>
           <li>Martinique (02)</li>
           <li>Île-de-France (11)</li>
           <li>Hauts-de-France (32)</li>
           <li>Centre-Val de Loire (24)</li>
           <li>Guadeloupe (01)</li>
           <li>Mayotte (06)</li>
           <li>Bretagne (53)</li>
    </p>
                
</body>
</html>
