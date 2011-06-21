from kivy.app import App
from controller import Controller
from lib.commandLineArgumentExtractor import tryToGetIdFromCommandLineArgument 
from lib.utils import Cursor

clientId = tryToGetIdFromCommandLineArgument()

class PlaneWhiteApp(App):
  def build(self):
    self.controller = Controller(cid=clientId)
    self.controller.add_widget(Cursor())
    return self.controller


  def on_stop(self):
    self.controller.cleanupOnExit()
    print "Closing connections."


PlaneWhiteApp().run()