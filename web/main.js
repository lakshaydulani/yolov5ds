window.onload = function () {

    $("#datepicker").datepicker({ maxDate: 0 });

    getDateData(getSelectedDate());

}

function getDateData(dat) {

    var dat = new Date();
    var year = dat.getFullYear();
    var month = dat.getMonth() + 1;
    var day = dat.getDate();
    var path = year + '-' + month + '-' + day + '.json';
    path = '2021-12-2.json';

    $("#selectedDate").text(friendlyDateFormat(dat));

    $.get("./../api/" + path, function (data) {
        window.cachedData = data;
        var emps = Object.keys(data);
        emps.forEach(function (emp) {
            $("#empList").append("<li><a onclick='selectEmployee(this)' href='javascript:void(0);'><img src='" + getEmpImage(emp) + "'><strong>" + emp + "</strong></a></li>");
        });
        $("#empList li:first a").click();
    });
}

function getEmpImage(name) {
    var path = name.toLowerCase().replace(/\s/g, '') + '.jpg';
    return "./images/" + path;
}

function getSelectedDate() {
    return new Date();
}

function selectEmployee(o) {
    $(o).parent().addClass("selected").siblings().removeClass("selected");
    var emp = $(o).text().trim();
    var empData = window.cachedData[emp];
    var totalTimeInHours = empData.totalTime.toFixed(2);
    $("#empProductivity").text(totalTimeInHours + " / 8 hours");
    $("#empProductivityPercent").text((totalTimeInHours * 12.5).toFixed(2) + " %");

    var dat = getSelectedDate();
    renderChart(totalTimeInHours, dat);

    $("#empInfo").removeClass("hidden");
}

// function to return human friendly date format
function friendlyDateFormat(dat) {
    var options = { year: 'numeric', month: 'long', day: 'numeric' };
    return dat.toLocaleDateString("en-US", options);
}

function renderChart(totalTimeInHours, dat) {

    var workingpercent = (totalTimeInHours / 8) * 100;

    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        // title: {
        //     text: friendlyDateFormat(dat)
        // },
        data: [{
            type: "pie",
            startAngle: 240,
            yValueFormatString: "##0.00\"%\"",
            indexLabel: "{label} {y}",
            dataPoints: [{
                y: workingpercent,
                label: "Productive"
            }, {
                y: (100 - workingpercent),
                label: "Unproductive"
            }]
        }]
    });
    chart.render();
}