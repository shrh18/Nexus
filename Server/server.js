// var http = require('http');
// var s = http.createServer();
// s.on('request', function(request, response) {
//     response.writeHead(200);
//     console.log('a: '+request.method);
//     console.log('b: '+request.headers);
//     console.log('c: '+request.url);

//     var url = decodeURIComponent(request.url);
//     var startPos = url.indexOf('{');
//     var endPos = url.indexOf('}');
//     var jsonString = url.substring(startPos, endPos+1);
//     // json = JSON.parse(jsonString);
//     // console.log(json['data'])
//     console.log(jsonString)
// });
// s.listen(3000);


// Import dependencies
const express = require('express');
const http = require('http');
const socketIO = require('socket.io');
const path = require('path');
const net = require('net');

// Create a new express app
const app = express();
const port = 12345;
const host = 'localhost';
const server = http.createServer(app);

// Create a new socket.io instance
const io = socketIO(server);
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'))


io.on('connection', socket => {
  console.log('a user connected');

  // Listen for data from the client
  socket.on('data', data => {
    console.log('data received:', data);
    fdata=data;
    // app.get('/', async(req, res) => {
    // res.render('dataPage', {data})
    // });

    // Broadcast the data to all connected clients
    io.emit('data', data);
  });

  // Listen for socket.io disconnections
  socket.on('disconnect', () => {
    console.log('user disconnected');
  });
});

// const serverPage = net.createServer();
// serverPage.listen(port, host, () => {
//     console.log('TCP Server is running on port ' + port +'.');
// });

let sockets = [];
let fdata;

// serverPage.on('connection', function(sock) {
//     console.log('CONNECTED: ' + sock.remoteAddress + ':' + sock.remotePort);
//     sockets.push(sock);

//     sock.on('data', function(data) {
//         console.log('DATA ' +  ': ' + data);
//         fdata = data;
//         // Write the data back to all the connected, the client will receive it as data from the server
//         sockets.forEach(function(sock, index, array) {
//             sock.write(sock.remoteAddress + ':' + sock.remotePort + " said " + data + '\n');
//         });
//     });
// });

app.get('/', async(req, res) => {
        res.render('dataPage', {fdata});
});

// serverPage.close()
app.listen(12345, () =>{
    console.log("Serving on port 12345");
})