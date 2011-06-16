from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import *

from lib.connectionToServer import Client
import lib.config

from lib.transitions import Fade

from mode1 import ScreenSaver
from mode2 import Learning
from mode3 import Discovering
from mode4 import Credits


class Controller(Widget):
  def __init__(self, **kwargs):
    super(Controller, self).__init__(**kwargs)
    self.clientId = kwargs.pop('cid', 1)
    self.modes = [ScreenSaver(controller=self),
                  Learning(controller=self),
                  Discovering(controller=self),
                  Credits(controller=self)]
                  
    self.startConnection()

    transition = Fade(dir=0, color=Color(0,0,0,1), fade_speed=0.1)
    self.add_widget(transition)
    self.add_widget(self.modes[0])
    transition.start()

  def sendMessage(self, message):
    print "Sending message ", message
    self.connection.sendMessage(message)
  

  def onNewMessageFromServer(self, message):
    print "new message from server:", message


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
