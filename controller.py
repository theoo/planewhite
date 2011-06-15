from kivy.uix.widget import Widget
from kivy.clock import Clock
from lib.connectionToServer import Client
import lib.config

class Controller(Widget):
  def __init__(self, **kwargs):
    super(Controller, self).__init__(**kwargs)
    self.clientId = kwargs.pop('cid', 1)
    self.scenes = []
    self.startConnection()


  def onNewMessageFromServer(self, message):
    print "new message from server:", message
    #parse.parseMessage(message, self.ball)

  def connectionListen(self, dt):
    self.connection.listen()

  def cleanupOnExit(self):
    self.connection.close() 

  def startConnection(self):
    self.connection = Client(host=config.host, port=config.port, callback=self.onNewMessageFromServer) 
    self.connection.connect()
    # send who we are
    self.connection.sendMessage(config.id)
    # start listening 
    Clock.schedule_interval(self.connectionListen, 0)
