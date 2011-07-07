var net = require('net'),
    carrier = require('carrier'), //carrier installs via npm
    world = require('./lib/world.js').World();


net.createServer(function(connection){


  // add property clientId to new connection
  var clientId;

  connection.getId = function(){
    return clientId;
  }


  connection.on('close', function(){
    world.removeClient(connection);
  });

  // we don't use connections.on('data',...) because we don't know what we get
  // a line, a some chars ??
  // we need to parse until we get a new line hence we use carrier module

  carrier.carry(connection, function(line){

    if(!clientId){
      clientId = parseInt(line);
      world.registerConnection(connection);
      return;
    }

    console.log("--------------------------------");
    console.log("we receive message from " + clientId); 
    console.log("message : " + line);


    if (line.toLowerCase() == "quit"){
      console.log("client " + clientId + " has disconnected")
      connection.end();
      return;
    }
    

    world.parseMessage(line, clientId);
  });
}).listen(4000);


console.log ("awaiting connections on port 4000");
