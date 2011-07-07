
var ModeHandler_4 = function(){

  this.parseMessage = function(message, clientId, world){

    switch(message){
      case "credits_touched":
        // special case goto mode 2 - canceled
        // world.gotoMode(2);
        world.gotoNextMode();
        break;
      case "credits_timeout":
        world.gotoNextMode();
        break;
      default:
        console.log("ModeHandler_4 has not been able to parse message: " + message); 
    }
  };
}



exports.ModeHandler_4 = function(){
  return new ModeHandler_4();
}

