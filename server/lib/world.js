// global config
// numOfClients needed to start system
// total number of modes
// TODO: refactor numOfModes in a modeManager


var modeHandler_1 = require('./modeHandler_1.js').ModeHandler_1(),
    modeHandler_2 = require('./modeHandler_2.js').ModeHandler_2(),
    modeHandler_3 = require('./modeHandler_3.js').ModeHandler_3(),
    modeHandler_4 = require('./modeHandler_4.js').ModeHandler_4(),
    numOfClients = 4,
    numOfModes = 4;  // should equal number of modeHandlers, not true while developing


var World = function(){
  
  var modeHandlers = [modeHandler_1, modeHandler_2, modeHandler_3, modeHandler_4],
      connections = [],
      worldIsReady = false,
      currentModeId = 1,
      currentModeHandler = modeHandlers[0];



  //public methods

  this.getNumOfConnectedClients = function(){
    return connections.length;
  }




  this.parseMessage = function(message, clientId){
    currentModeHandler.parseMessage(message, clientId, this);
  }




  this.registerConnection = function(connection){

    // connection validations
    // validations
    if (isNaN(connection.getId())){
      console.log("WARNING: WORLD.js :client id does not resolve to a number");
      console.log("disregarding connection");
      return;
    }

    if (inConnectedClients(connection)){
      console.log("WARNING: WORLD.js :this is already connected");
      console.log("disregarding connection");
      return;
    }

    if (connection.getId() < 1 || connection.getId() > numOfClients){
      console.log("WARNING: WORLD.js : screenId is illegal not in range 1..4");
      console.log("disregarding connection");
      return;
    }

    connections.push(connection);

    checkIfWorldIsReady();

    console.log("we are connected with " + connection.getId() + "\n");
  }




  this.removeClient = function(connection){
    var pos = connections.indexOf(connection);
    if(pos >= 0){
      connections.splice(pos, 1);
    }

    checkIfWorldIsReady();
  }


  this.gotoMode = function(modeId){
    console.log("--------------------gotoMode --> " + modeId);
    currentModeId = modeId;
    sendMessageForGoto();
    //currentModeHandler = getCurrentModeHandler();

    //var message = "change_mode/" + currentModeId;
    //sendMessageToAll(message);
  }


  this.gotoNextMode = function(){
    console.log("-------------------gotoNextMode");    
    currentModeId = getNextModeId();
    sendMessageForGoto();
    //currentModeHandler = getCurrentModeHandler();

    //var message = "change_mode/" + currentModeId;
    //sendMessageToAll(message);
  }

  var sendMessageForGoto = function(){
    currentModeHandler = getCurrentModeHandler();

    var message = "change_mode/" + currentModeId;
    sendMessageToAll(message);
  }



  this.sendMessageToNextClient = function(clientId, message){
    var nextClientId = getNextClientId(clientId),
        client = getClientById(nextClientId);

    while(client == -1){
      nextClientId = getNextClientId(nextClientId);
      client = getClientById(nextClientId);

      if (connections.length == 0){
        //noOne to send message to
        console.log("Warning can't send message to next client because nobody is connected");
        return;
      }
    }

    sendMessage(client, message);
  }


  this.sendMessageToAll = function(message){
    sendMessageToAll(message);
  }

  this.sendMessageToClient = function(clientId, message){
    var client = getClientById(clientId);
    world.sendMessage(client, message);
  }




  ///////////
  // private methods
  //


  var inConnectedClients = function(connection){
    var id = connection.getId();
    for (var i = 0, s = connections.length; i < s; i++){
      if (connections[i].getId() == id){
        return true;
      }
    }
    return false;
  }


  
  
  var sendMessageToAll = function(message){
    message = message + '\n';

    console.log("sending message to all clients: " + message);

    connections.forEach(function(a_connection){
      a_connection.write(message);
    });  
  }

  
  
  var sendMessage = function(client, message){

    if(client){
      console.log("sending message to client id: " + client.getId() + " --> " + message);
      client.write(message + '\n');
    }else{
      console.log("message not sent because client not found");
    }
  }


  
  var sendMessageToClientWithId = function(clientId, message){
    var client = getClientById(clientId);
    sendMessage(client, message);
  }

  
  
  var getClientById = function(id){
    var connection;
    for(var i = 0, s = connections.length; i < s; i++){
      connection = connections[i];
      if (connection.getId() == id){
        return connection;
      }
    }
      
    console.log("WARNING World.getConnectionById() failed to find connection for id " + id);
    return -1;
    //throw Error("fatal :: World.getConnectionById() failed to find connection for id " + id);
  }


  
  
  var getNextModeId = function(){
    var nextModeId = currentModeId + 1;
    if (nextModeId > numOfModes){
      nextModeId = 1;
    }

    return nextModeId;
  }

  
  
  
  var getNextClientId = function(id){

    var nextId = id + 1;
    if (nextId > numOfClients){
      nextId = 1;
    }
    
    return nextId;
  }

  
  
  
  var checkIfWorldIsReady = function(){
    if (connections.length == numOfClients){
      worldIsReady =  true;
      console.log("world is ready");
      startWorld();
    } else {
      worldIsReady = false;
      console.log("world is not ready resetting mode id");
      reset();
    }
  }

  
  var reset = function(){
    console.log("reseting world, we go back to mode 1");
    currentModeId = 1;
    currentModeHandler = getCurrentModeHandler(); 

    sendMessageToAll("reset_all");
  }

  
  var startWorld = function(){
    sendMessageToAll("change_mode/1");
  }

  
  
  var getCurrentModeHandler = function(){
    //TODO: handle over/underflow
    return modeHandlers[currentModeId - 1];
  }


  var toString = function(value){
    return value + '';
  }
}


//commonjs export statement
exports.World = function(){
  return new World();
}
