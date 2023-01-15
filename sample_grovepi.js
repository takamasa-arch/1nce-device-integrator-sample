const dgram = require('dgram');
const client = dgram.createSocket('udp4');
let message = ''

var {PythonShell} = require('python-shell');

PythonShell.run('./lib/get_dht11.py', null, function (err, result) {
    if (err) throw err;
 
    console.log(result);
    message = Buffer.from('temp:' + result[1] + ', humi:' + result[2]);

});

client.send(message, process.env.UDP_PORT_TEST || 4445, '127.0.0.1', (err) => {
    if (err) console.err(err);
    client.close();
    return 'done';
   });
   
