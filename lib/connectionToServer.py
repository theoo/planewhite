##client.py
import socket
import signal
import sys

newline = '\n'

class Client(object):

  def __init__(self, host, port, callback):
    # callback is called when we have new message
    self.host = host
    self.port = port
    self.address = (self.host, self.port)
    self.callback = callback
    self.data = ""
    self.connected = False
    signal.signal(signal.SIGINT, self.onQuit)
    

  def connect(self):
    try:
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.socket.connect(self.address)
    except socket.error, e:
      print "WARNING could not connect to server"
      return  # we return instead of exiting  see sendMessage and listen for
      #sys.exit(0)
    self.socket.setblocking(0)
    self.connected = True

  def sendMessage(self, message):
    # TODO:mmmmmmmmmm
    if not self.connected:
      return

    #check that data is string
    if not isinstance(message, basestring):
      message = str(message)
      print "WARNING Client.send called with non string argument"
    #check that message ends with newline
    if message[-1] != newline:
      message = message + newline

    print "sending message", message

    self.socket.setblocking(1)
    self.socket.send(message)
    self.socket.setblocking(0)



  def listen(self):
    try: 
      self.data += self.socket.recv(4096)
    except:
      return

    messages = [] # not really used since we send each message separetely to callback
    while '\n' in str(self.data):
      splitList = self.data.split('\n', 1)
      message = splitList[0]
      self.data = splitList[1]
      messages.append(message)
      self.callback(message)


  def close(self):
    self.sendMessage("QUIT")
    self.socket.close()

  def onQuit(self, signal, frame):
    print "catched ctr-c quitting and closing socket"
    self.close()
    sys.exit(0)

if __name__ == '__main__':

  def dummyCallback(message):
    print message
    pass

  client = Client('localhost', 4000, dummyCallback)
  client.connect()
  client.send("LEFT\n")

  while 1:
    print "update"
    client.listen()


#HOST = 'localhost'
#PORT = 4000    #our port from before
#ADDR = (HOST,PORT)
# 
#cli = socket(AF_INET,SOCK_STREAM)
#cli.connect((ADDR))
#
#data = ""
#
#while 1:
#    
#  data += cli.recv(100)
#
#  messages = []
#  while '\n' in str(data):
#    splitList = data.split('\n', 1)
#    message = splitList[0]
#    data = splitList[1]
#    messages.append(message)
#    
#  for m in messages:
#    print "new message", m
#
#  #print "rest", data
#
#
#
##data = cli.recv(BUFSIZE)
##print data
##
##cli.close()
