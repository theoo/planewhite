from kivy.uix.widget import Widget
from kivy.clock import Clock
from lib.connectionToServer import Client
import lib.config

from mode1 import ScreenSaver

class Controller(Widget):
  def __init__(self, **kwargs):
    super(Controller, self).__init__(**kwargs)
    self.clientId = kwargs.pop('cid', 1)
    self.modes = [ScreenSaver()]
    self.startConnection()

    self.add_widget(self.modes[0])



  def onNewMessageFromServer(self, message):
    print "new message from server:", message
    #parse.parseMessage(message, self.ball)

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
