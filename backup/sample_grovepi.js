const dgram = require('dgram');
const client = dgram.createSocket('udp4');

let message = ''

var {PythonShell} = require('python-shell');

for (var i=0;i<3;i++){

    PythonShell.run('./lib/get_dht11.py', null, function (err_p, result) {
        if (err_p) throw err_p;
        
        message = Buffer.from('temp:' + result[1] + ', humi:' + result[2]);
    
        client.send(message, process.env.UDP_PORT_TEST || 4445, '127.0.0.1', (err) => {
            if (err) {
                console.err(err);
                client.close();
            }
            else{
                console.log(console.log(result));
            }
        });
    
    })

    console.log(i);
    if (i==2) {
        console.log('end!');
        return;
    }

    PythonShell.run('./lib/sleep.py', null, function (err_p, result) {
        if (err_p) throw err_p;
    })

};
