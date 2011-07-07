

var ModeHandler_2 = function(){

  var screenCounter = 0;

  this.parseMessage = function(message, clientId, world){

    switch(message){
      case "threshold_reached":
        screenCounter += 1;
        
        // check if we received message from everyone
        if (screenCounter >= (world.getNumOfConnectedClients() )){
          screenCounter = 0;
          world.gotoNextMode();
        }
        break;

      default:
        console.log("ModeHandler_2 has not been able to parse message: " + message); 
    }
  };
}



exports.ModeHandler_2 = function(){
  return new ModeHandler_2();
}

