const csv = require('csv-parser');
const fs = require('fs');
const config = require('./config.js');
const utils = require('./utils.js');

const employees = {};
config.employees.forEach(employee => { employees[employee] = { 'timestamps': [] }; });

fs.createReadStream('./../Yolov5_DeepSort_Pytorch/data.csv')
  .pipe(csv())
  .on('data', (row) => {
    var names = row.Employees;
    var time = new Date(row.Time);

    Object.keys(employees).forEach(employee => {
      var typ = names.includes(employee) ? 'in' : 'out';
      employees[employee]['timestamps'].push({ 'type': typ, 'time': time });
    });
  })
  .on('end', () => {

    Object.keys(employees).forEach(employee => {
      const timestamps = employees[employee]['timestamps'];
      employees[employee]['totalTime'] = utils.getTotalTime(timestamps);
    });

    fs.writeFile(`${utils.getCurrentTimestamp()}.json`, JSON.stringify(employees), 'utf8', function () {
      console.log('file saved successfully');
    });
  });