var utils = {};


// function to get current timestamp path in the format of YYYY-MM-DD-HH-MM-SS
utils.getCurrentTimestamp = function () {
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();
    var timestamp = year + '-' + month + '-' + day;
    return timestamp;
};


utils.getTotalTime = function (timestamps) {
    var total = 0;
    var lastTime = timestamps[0];
    var lookingFor = 'out';
    for (var i = 1; i < timestamps.length; i++) {
        var timestamp = timestamps[i];
        if (lookingFor === 'in' && timestamp.type === 'in') {
            lastTime = timestamp;
            lookingFor = 'out';
            continue;
        }
        if (timestamp.type === lookingFor) {
            var time = getTimeDifference(lastTime.time, timestamp.time);
            total += time;
            lookingFor = (lookingFor === 'out') ? 'in' : 'out';
        }
    }
    return total / (60); // return in time in minutes

    function getTimeDifference(date1String, date2String) {
        const date1 = new Date(date1String);
        const date2 = new Date(date2String);
        const difference = date2.getTime() - date1.getTime();
        const secondsDifference = Math.floor(difference / (1000));
        return secondsDifference;
    }
};

module.exports = utils;