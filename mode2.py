# ScreenSaver

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.app import App

from kivy.clock import Clock
from kivy.animation import Animation

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
#from kivy.core.image import Image

from kivy.graphics import *

# Configuration

class Learning(Widget):
  
  def __init__(self, **kwargs):
    super(Learning, self).__init__(**kwargs)  
    self.img = Image(source="../images/kand8_1.jpg", size=(1024,768), color=[1,1,1,0.5], pos=(0,0))  
    self.points = []
        
  def on_touch_down(self, touch):
    self.draw_ellipse(touch)
    
  def on_touch_move(self, touch):
    self.draw_ellipse(touch)
    
  def on_touch_up(self, touch):
    pass    

  def draw_ellipse(self, touch):
    # Use this instead of "append" if you are displaying Point cloud.
    # self.points += touch.pos
    
    self.points.append(touch.pos)

    # required, this fix a performance issue.
    self.canvas.clear()
       
    with self.canvas:
      StencilPush()
      # One easy solution
      # Point(pointsize=20., points=self.points)
      
      # This is slower than Point but still usable
      # Todo: improve perfs by discarding position tuple already existing in the array.
      for pos in self.points:
        diameter = 100
        Ellipse(pos=(pos[0] - diameter / 2, pos[1] - diameter / 2), size=(diameter, diameter))
      
      StencilUse()
      Image(source="../images/kand8_1.jpg", size=(1024,768), color=[1,1,1,1], pos=(0,0))
      
      StencilPop()      
    
      
class LearningApp(App):
    def build(self):      
      base = Widget()
      base.add_widget(Learning())
      
      return base
      
if __name__ == '__main__':
    LearningApp().run()
