//**************************************************//
// Showing data on the grid
//**************************************************//

const file = document.getElementById('file')
const reader = new FileReader()

reader.addEventListener("load", function(e) {
    const csv = event.target.result
    const data = d3.csvParse(csv);

    //var csv1 = CSVToArray(data);
    renderCSVDropdown(data);
     //Submit File form
    //debugger;
    $('form#myFile').submit()

    d3.select("body")
        .append("table")
        .attr("id", "myTable")
        .append("thead")
        .append("tr")
        .html(function(d) {
            return data.columns.map((text) => `<th>${text.trim()}</th>`).join("\n")
        })

    const rows = d3.select("#myTable")
        .append("tbody")
        .selectAll("tr")
        .data(data).enter()
        .append("tr")
        .each(function(d) {
            d3.select(this)
                .selectAll("td")
                .data(function(row) {
                    return data.columns.map(function(column) {
                        return { column: column, value: row[column] };
                    })
                })
                .enter()
                .append("td")
                .html(function(d) { return d.value.trim() });
        })
})

file.addEventListener('change', function(e) {
    const f = e.target.files[0]
    reader.readAsText(f)
});

//**************************************************//
// Populating drop down menus from csv file
//**************************************************//
function renderCSVDropdown(csv){
    var dropdown = $('select#id, select#label, select#time-series, select#dimension,select#fact');

    var record = csv[0];
    var keys = Object.keys(record);
        for(var i = 0; i < keys.length; i++) {
            var option = $('<option value="'+keys[i]+'">'+keys[i]+'</option>');
            //var entry = $('<option>').attr('value', keys[i]);
            dropdown.append(option);
        }
}


function CSVToArray( strData, strDelimiter ){
    // Check to see if the delimiter is defined. If not,
    // then default to comma.
    strDelimiter = (strDelimiter || ",");

    // Create a regular expression to parse the CSV values.
    var objPattern = new RegExp(
        (
            // Delimiters.
            "(\\" + strDelimiter + "|\\r?\\n|\\r|^)" +

            // Quoted fields.
            "(?:\"([^\"]*(?:\"\"[^\"]*)*)\"|" +

            // Standard fields.
            "([^\"\\" + strDelimiter + "\\r\\n]*))"
        ),
        "gi"
        );

    // Create an array to hold our data. Give the array
    // a default empty first row.
    var arrData = [[]];

    // Create an array to hold our individual pattern
    // matching groups.
    var arrMatches = null;


    // Keep looping over the regular expression matches
    // until we can no longer find a match.
    while (arrMatches = objPattern.exec( strData )){

        // Get the delimiter that was found.
        var strMatchedDelimiter = arrMatches[ 1 ];

        // Check to see if the given delimiter has a length
        // (is not the start of string) and if it matches
        // field delimiter. If id does not, then we know
        // that this delimiter is a row delimiter.
        if (
            strMatchedDelimiter.length &&
            strMatchedDelimiter !== strDelimiter
            ){

            // Since we have reached a new row of data,
            // add an empty row to our data array.
            arrData.push( [] );

        }

        var strMatchedValue;

        // Now that we have our delimiter out of the way,
        // let's check to see which kind of value we
        // captured (quoted or unquoted).
        if (arrMatches[ 2 ]){

            // We found a quoted value. When we capture
            // this value, unescape any double quotes.
            strMatchedValue = arrMatches[ 2 ].replace(
                new RegExp( "\"\"", "g" ),
                "\""
                );

        } else {

            // We found a non-quoted value.
            strMatchedValue = arrMatches[ 3 ];

        }


        // Now that we have our value string, let's add
        // it to the data array.
        arrData[ arrData.length - 1 ].push( strMatchedValue );
    }

    // Return the parsed data.
    return( arrData );
}