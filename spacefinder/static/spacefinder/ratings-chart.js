google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

// Format all the iso dates to Hour:Minute:Second format
// [TODO] There must be a way to do this in Python instead of this bullshti
// workaround
var latest_ratings = latest_ratings.map(function(n) {
    return [moment(new Date(n[0])).format('hh:mm'), n[1]];
});

latest_ratings.unshift(["Time", "Rating"]);
console.log(latest_ratings);


var days_ratings = days_ratings.map(function(n) {
    return [moment(new Date(n[0])).format('hh:mm'), n[1]];
});


days_ratings.unshift(["Time", "Rating"]);

console.log(days_ratings);

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

    var latest_ratings_graph = new google.visualization.LineChart(document.getElementById('latest_ratings_graph'));
    latest_ratings_graph.draw(google.visualization.arrayToDataTable(latest_ratings), options);

    var days_ratings_graph = new google.visualization.LineChart(document.getElementById('days_ratings_graph'));
    days_ratings_graph.draw(google.visualization.arrayToDataTable(days_ratings), options);
}

