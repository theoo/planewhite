
var ModeHandler_3 = function(){

  var screenCounter = 0

  this.parseMessage = function(message, clientId, world){

    switch(message){
      case "all_zones_of_interest_viewed":
        screenCounter |= (1 << (clientId - 1)); // from 0 to 3
        
        if (screenCounter == 0x000F) { // 32 bits integer = 16
          screenCounter = 0;
          // wait 5 seconds.
          timeoutID = setTimeout(function() {
              world.gotoNextMode();
          }, 5000);
        }
        
        // check if we received message from everyone
        /*
        if (screenCounter >= (world.getNumOfConnectedClients() )){
          screenCounter = 0;
          world.gotoNextMode();
        }
        */
        
        break;
      default:
        console.log("ModeHandler_3 has not been able to parse message: " + message); 
    }
  };
}



exports.ModeHandler_3 = function(){
  return new ModeHandler_3();
}

