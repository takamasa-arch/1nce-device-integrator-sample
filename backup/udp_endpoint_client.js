const dgram = require('dgram');

const message = Buffer.from('Hello World');
const client = dgram.createSocket('udp4');

client.send(message, process.env.UDP_PORT_TEST || 4445, '127.0.0.1', (err) => {
 if (err) console.err(err);
 client.close();
 return 'done';
});

