google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {

    var options = {
        backgroundColor: 'transparent',
        legend: 'none',
        hAxis: {
            textStyle: {
                fontSize: 12,
                fontName: 'museo-sans-rounded',
                bold: true,
            },
        },
        vAxis: {
            gridlines: {
                color: 'transparent'
            },
            textStyle: {
                fontSize: 10,
                fontName: 'museo-sans-rounded',
                bold: true,
            },
        },

        colors: ['#FCB12D'],
        chartArea: {
            width: 270,
        },
    };

    top_student_voters.unshift(["User", "Rating"]);
    var top_student_voters_chart = new google.visualization.ColumnChart(document.getElementById('top-student-voters-chart'));
    top_student_voters_chart.draw(google.visualization.arrayToDataTable(top_student_voters), options);

}
