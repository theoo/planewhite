from kivy.uix.widget import Widget
from kivy.clock import Clock
from lib.connectionToServer import Client
import lib.config

from mode1 import ScreenSaver

class Controller(Widget):
  def __init__(self, **kwargs):
    super(Controller, self).__init__(**kwargs)
    self.clientId = kwargs.pop('cid', 1)
    self.modes = [ScreenSaver(controller=self, modeId=1)]
    self.currentModeId = -1
    self.startConnection()



  def sendMessage(self, message):
    self.connection.sendMessage(message)




  def stopCurrentMode(self):
    if self.currenModeId == -1:
      return

    self.currentMode.stop()
    self.remove_widget(self.currentMode)



  def startCurrentMode(self):
    self.add_widget(self.currentMode)
    self.currentMode.stop()
  


  # messages from server arrive here
  #
  def onNewMessageFromServer(self, message):
    print "new message from server:", message
    #
    # mr piggy was here...
    if message == "change_mode/1":
      self.stopCurrentMode()
      self.currenModeId = 1 # this must be called after stopCurrentMode() !!
      self.updateCurrentMode()
      self.startCurrentMode()



  def updateCurrentMode():
    self.currentMode = self.modes[self.currentModeId - 1]  



  # connection stuff
  #
  def connectionListen(self, dt):
    self.connection.listen()

  def cleanupOnExit(self):
    self.connection.close() 

  def startConnection(self):
    self.connection = Client(host=lib.config.host, port=lib.config.port, callback=self.onNewMessageFromServer) 
    self.connection.connect()
    # send who we are
    self.connection.sendMessage(self.clientId)
    # start listening 
    Clock.schedule_interval(self.connectionListen, 0)
