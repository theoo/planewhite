from kivy.app import App
from controller import Controller
from lib.commandLineArgumentExtractor import tryToGetIdFromCommandLineArgument 

clientId = tryToGetIdFromCommandLineArgument()

class PlaneWhiteApp(App):
  def build(self):
    self.controller = Controller(cid=clientId)
    return self.controller


  def on_stop(self):
    self.controller.cleanupOnExit()
    print "onClose"




PlaneWhiteApp().run()

