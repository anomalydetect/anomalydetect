// Showing data on the grid
const file = document.getElementById('file')
const reader = new FileReader()

reader.addEventListener("load", function(e) {
    const csv = event.target.result
    const data = d3.csvParse(csv);

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


