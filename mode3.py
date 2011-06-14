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

class Discovering(Widget):

  def __init__(self, **kwargs):
    super(Discovering, self).__init__(**kwargs)
    with self.canvas:
      Image(source="../images/kand8_1.jpg", size=(1024,768), color=[1,1,1,0.2], pos=(0,0))
      d = 100
      Color(1,1,1)
      Ellipse(size=(d,d), pos=(103 - d/2,236 - d/2))
      Point(pointsize=10, points=(286.0,521.0))
      
  def on_touch_down(self, touch):
    pass
    
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
