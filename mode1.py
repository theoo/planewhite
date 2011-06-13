# ScreenSaver

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.app import App

from kivy.clock import Clock
from kivy.animation import Animation

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from kivy.graphics import *

# Configuration
SCAN_IMG_PATH = '../images/scan.png'
SCAN_DURATION = 2


class ScreenSaver(Widget):
  
  def __init__(self, **kwargs):
    """docstring for fname"""
    super(ScreenSaver, self).__init__(**kwargs)  
    
    self.img = Image(source=SCAN_IMG_PATH, size=(218,768), color=[1,1,1,0.5], pos=(0,0))
    self.add_widget(self.img)

    Clock.schedule_interval(self.scan, SCAN_DURATION)


  def scan(self, dt):
    self.img.pos = (0,0)
    a = Animation(pos=(Window.width, 0), duration=SCAN_DURATION)
    a.start(self.img)


  def on_touch_move(self, touch):
    pass #debug
      
      
class ScreenSaverApp(App):
    def build(self):
      base = Widget()
      base.add_widget(ScreenSaver())
      return base
      
if __name__ == '__main__':
    ScreenSaverApp().run()
