$(document).ready(function(){
    $.get("/api/meta/all", function(countrydata) {
        for (var countrycode in countrydata) {
            $("<option/>", {value: countrycode, html: countrydata[countrycode].name})
                    .appendTo("select#countryselect");
        }
    });

    $("form#searchform").submit(function(e) {
        e.preventDefault();


        $.get("/api/country/" + $("#countryselect").val() + "?" + $("#searchform").serialize(), draw_chart);
    });

});

function draw_chart(data) {
    var countrycode = Object.keys(data)[0];
    var zipped = zip(data[countrycode]);
    var years  = zipped[0],
        values = zipped[1];


    var ispercapita = $("input[name=percapita]").is(":checked");
    var yaxislabel = ispercapita ? "CO2 emissions per capita (kt)" : "CO2 emissions (kt)";

    var ctx = document.getElementById("chart").getContext("2d");
    var chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: years,
            datasets: [{
                label: countrycode,
                data: values
            }]
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: yaxislabel
                    }
                }]
            }
        }
    });
}

function zip(arrays) {
    return arrays[0].map(function(_,i){
        return arrays.map(function(array){return array[i]})
    });
}
