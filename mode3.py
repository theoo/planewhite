# ScreenSaver

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.app import App

from kivy.clock import Clock
from kivy.animation import Animation

from kivy.uix.stencilview import StencilView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from kivy.graphics import *

# Configuration

class ZoneOfInterest(Widget):
  def __init__(self, obj=None, desc=None, pos=(0,0), **kwargs):
    super(ZoneOfInterest, self).__init__(**kwargs)
    
    self.canvas.add(obj)
    
    self.object = obj
    self.desc = desc
    self.pos = pos
  
    self.object.pos = self.pos  


class Discovering(Widget):

  def __init__(self, **kwargs):
    super(Discovering, self).__init__(**kwargs)
      
    # First item of self.shapes is the background
    with self.canvas:
      Image(source="images/kand8_1.jpg", size=(1024,768), color=[1,1,1,0.2], pos=(0,0))

    # zones of interest
    self.shapes = []
    self.shapes.append( ZoneOfInterest( Ellipse(size=(100,100)),
                                        "This is a demonstration.",
                                        (53,186) ) )

    self.shapes.append( ZoneOfInterest( Rectangle(size=(20,100)),
                                        "This is a demonstration.",
                                        (320,500) ) )

    
    for shape in self.shapes:
      # add shape to view
      # self.canvas.add(Color(1.,1.,1.,0.))
      self.add_widget(shape)
      
      # add animation
      
      
  def on_touch_down(self, touch):
    for shape in self.shapes:
      # add interaction
      if shape.collide_point(*touch.pos):
        print "touched " + str(shape.pos)
        
  def on_touch_move(self, touch):
    pass
    
  def on_touch_up(self, touch):
    pass
    
      
class DiscoveringApp(App):
    def build(self):
      base = Widget()
      base.add_widget(Discovering())
      
      return base
      
if __name__ == '__main__':
    DiscoveringApp().run()
