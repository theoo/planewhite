
var ModeHandler_1 = function(){

  this.parseMessage = function(message, clientId, world){
    timouteID = false;
    
    switch(message){
      case "scan_end":
        
        // wait a while to make it "scanner"

        if (clientId == 4) // don't know how to access numOfClients variable from here without modifying parseMessage()
        {
          console.log("Waiting 2 sec before starting again the loop.");
          timeoutID = setTimeout(function() {
            world.sendMessageToNextClient(clientId, "scan_start");
          }, 2000);
          console.log(timeoutID);
          break;
        } 
        else
        {
          world.sendMessageToNextClient(clientId, "scan_start");
          break;          
        }

  
      case "screensaver_touched":

        if (timeoutID)
        {
          clearTimeout(timeoutID);
        }
        // synchronize fadeIn
        world.sendMessageToAll("scan_fadein");

        // wait ten seconds before switching to next mode
        console.log("Waiting 10 sec before switching.");
        timeoutID = setTimeout(function() {
            world.gotoNextMode();
        }, 5000);
        break;
                      
      default:
        console.log("ModeHandler_1 has not been able to parse message: " + message); 
    }
  };
}



exports.ModeHandler_1 = function(){
  return new ModeHandler_1();
}

