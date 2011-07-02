from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import *

from lib.connectionToServer import Client
import lib.config

from mode1 import ScreenSaver
from mode2 import Learning
from mode3 import Discovering
from mode4 import Credits


class Controller(Widget):
  def __init__(self, **kwargs):
    super(Controller, self).__init__(**kwargs)
    self.clientId = kwargs.pop('cid', 1)
    
    self.modes = [ScreenSaver(controller=self, modeId=1),
                  Learning(controller=self, modeId=2),
                  Discovering(controller=self, modeId=3),
                  Credits(controller=self, modeId=4)]

    self.currentModeId = -1

    self.startConnection()
    self.serverIsReady = False

  # messages from server arrive here
  #
  def onNewMessageFromServer(self, message):
    print "new message from server:", message

    if message == "reset_all":
      #TODO cleanup serverIsReady hack
      self.serverIsReady = False

      self.stopCurrentMode()
      self.reset_all_modes()
      self.currentModeId = -1

    elif message == "change_mode/1": # mode 1 messages
      self.serverIsReady = True

      self.stopCurrentMode()
      self.currentModeId = 4
      self.updateCurrentMode()
      self.add_widget(self.currentMode)
      # only start if we are numero uno      
#      if self.clientId == "1":
#        self.currentMode.start()

      self.currentMode.start()

    elif message == "scan_start":
      if self.serverIsReady:
        self.currentMode.start()

    elif message == "scan_fadein":
      if self.serverIsReady:
        self.currentMode.fadein()
   
    elif message == "change_mode/2": # mode 2 messages
      self.stopCurrentMode()
      self.currentModeId = 2
      self.updateCurrentMode()
      self.add_widget(self.currentMode)
      self.currentMode.start()

    elif message == "change_mode/3": # mode 3 messages
      self.stopCurrentMode()
      self.currentModeId = 3
      self.updateCurrentMode()
      self.add_widget(self.currentMode)
      self.currentMode.start()

    elif message == "change_mode/4":
      self.stopCurrentMode()
      self.currentModeId = 4
      self.updateCurrentMode()
      self.add_widget(self.currentMode)
      self.currentMode.start()

    else:
      print "message is not recognized:", message


  def sendMessage(self, message):
    print "Sending message ", message
    self.connection.sendMessage(message)


  def stopCurrentMode(self):
    if self.currentModeId == -1:
      return

    self.currentMode.stop()
    self.remove_widget(self.currentMode)
    
  
  def reset_all_modes(self):
    for mode in self.modes:
      mode.reset()
    

  def updateCurrentMode(self):
    # TODO: check over/under flows
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
