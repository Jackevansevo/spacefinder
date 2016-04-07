google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

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

    latest_ratings.unshift(["Time", "Rating"]);
    var latest_ratings_chart = new google.visualization.LineChart(document.getElementById('latest-ratings-chart'));
    latest_ratings_chart.draw(google.visualization.arrayToDataTable(latest_ratings), options);
}
