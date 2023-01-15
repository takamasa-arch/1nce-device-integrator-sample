const dgram = require('dgram');
const client = dgram.createSocket('udp4');

var {PythonShell} = require('python-shell');

PythonShell.run('./lib/get_dht11.py', null, function (err, result) {
    if (err) throw err;
 
    console.log(result);
//    let message = Buffer.from(result[1]);

});

