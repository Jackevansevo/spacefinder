google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

// // Format all the iso dates to Hour:Minute:Second format
var data = data.map(function(n) {
    return [moment(new Date(n[0])).format('hh:mm'), n[1]];
});

data.unshift(["Time", "Rating"]);

function drawChart() {

    var options = {
        curveType: 'function',
        pointSize: 7,
        backgroundColor: 'transparent',
        legend: 'none',
        hAxis: {
            maxAlternation: 1,
            maxTextLines: 1,
            slantedText: 'false',
        },
        vAxis: {
            gridlines: {
                color: 'transparent'
            },
            ticks: [
                {v: 0, f: ''},
                {v: 1, f: 'Busy'},
                {v: 2, f: 'Quite-Busy'},
                {v: 3, f: 'Average'},
                {v: 4, f: 'Quite-Empty'},
                {v: 5, f: 'Empty'}
            ],
            format: '#',
        }
    };

    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

    chart.draw(google.visualization.arrayToDataTable(data), options);
}

