# Credits

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.app import App

from kivy.clock import Clock
from kivy.animation import Animation

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from kivy.graphics import *

# Configuration
BACKGROUND = "images/bgs/2.jpg"

class Credits(Widget):
  
  def __init__(self, **kwargs):
    super(Credits, self).__init__(**kwargs)  
    self.img = Image(source=BACKGROUND, size=(1024,768), color=[1,1,1,0.5])  
    self.add_widget(self.img)
        
  def on_touch_down(self, touch):
    pass
    
  def on_touch_move(self, touch):
    pass
    
  def on_touch_up(self, touch):
    pass    
    
      
class CreditsApp(App):
    def build(self):      
      base = Widget()
      base.add_widget(Credits())
      
      return base
      
if __name__ == '__main__':
    CreditsApp().run()
