# transistions

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.app import App

from kivy.clock import Clock

from kivy.graphics import *


class Fade(Widget):

  def __init__(self, **kwargs):
    super(Fade, self).__init__(**kwargs)
    
    # set defaults
    self.color = Color(0,0,0,0)
    self.background = Rectangle(size=Window.size)
    self.alpha_index_step = 0.01
    self.fade_speed = 0.01
    self.dir = 1 # Fade IN

    if self.dir:
      self.alpha_index = 0.0
    else:
      self.alpha_index = 1.0

    # apply custom setting sent as arguments
    for key, value in kwargs.iteritems():
      if hasattr(self, key):
        setattr(self, key, value)
    
    if __name__ == '__main__':
      self.start()
     
      
# basis  
  def start(self):
    if self.dir:
      Clock.schedule_once(self.In, 0)      
    else:
      Clock.schedule_once(self.Out, 0)
      
          
  def stop(self):
    pass
    
    
# Custom methods
  def In(self, instance=False):
    self.alpha_index += self.alpha_index_step
    self.color.a = self.alpha_index
    
    self.updateCanvas()
    
    if self.alpha_index <= 1.0:
      Clock.schedule_once(self.In, self.fade_speed)
    else:
      print "reached full opacity"
      
  
  def Out(self, instance=False):
    self.alpha_index -= self.alpha_index_step
    self.color.a = self.alpha_index
    
    self.updateCanvas()
        
    if self.alpha_index > 0.0:
      Clock.schedule_once(self.In, self.fade_speed)
    else:
      print "reached full transparency"
      
      
  def updateCanvas(self):
    self.canvas.clear() 
    self.canvas.add(self.color)
    self.canvas.add(self.background)    
    
if __name__ == '__main__':
  class FadeApp(App):
    def build(self):
      return Fade(color=Color(0,1,0,1))
    
  FadeApp().run()