google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

// Function to draw Google Charts
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

    // Creates chart showing the latest Ratings
    latest_ratings.unshift(["Time", "Rating"]);
    var latest_ratings_graph = new google.visualization.LineChart(document.getElementById('latest_ratings_graph'));
    latest_ratings_graph.draw(google.visualization.arrayToDataTable(latest_ratings), options);

    // Creates chart showing ratings from the last number of days
    days_ratings.unshift(["Time", "Rating"]);
    var days_ratings_graph = new google.visualization.LineChart(document.getElementById('days_ratings_graph'));
    days_ratings_graph.draw(google.visualization.arrayToDataTable(days_ratings), options);
}

