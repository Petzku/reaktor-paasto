$(document).ready(function(){
    console.log("doc ready")
    $.get("/api/meta/all", function(countrydata) {
        for (var countrycode in countrydata) {
            $("<option/>", {value: countrycode, html: countrydata[countrycode].name})
                    .appendTo("select#countryselect");
        }
    });

    $("form#searchform").submit(function(e) {
        e.preventDefault();

        $.get("/api/country/" + $("#countryselect").val() + "?" + $("#searchform").serialize(), function(data){
            // TODO

        });
    });

});
