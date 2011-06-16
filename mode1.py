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
SCAN_IMG_PATH = 'images/scan.png'
SCAN_DURATION = 2


class ScreenSaver(Widget):
  
  def __init__(self, **kwargs):
    super(ScreenSaver, self).__init__(**kwargs)  
    if kwargs.has_key("controller"):
      self.controller = kwargs.pop("controller")

    self.modeId = kwargs.pop("modeId") 
    self.img = Image(source=SCAN_IMG_PATH, size=(218,768), color=[1,1,1,0.5], pos=(0,0))
    self.add_widget(self.img)


  def start(self):
    print "start called on ScreenSaver"
    Clock.schedule_once(self.scan, 0)


  def stop(self):
    pass

  def scan(self, dt):
    self.img.pos = (0,0)
    a = Animation(pos=(Window.width, 0), duration=SCAN_DURATION)
    a.start(self.img)
    
    a.bind(on_complete=self.onAnimComplete)


  def onAnimComplete(self, animation, target):
    self.controller.sendMessage("scan_end") # sync next client


  def on_touch_down(self, touch):
    self.controller.sendMessage("screensaver_touched") # go to next mode

      
if __name__ == '__main__':
  class ScreenSaverApp(App):
      def build(self):
        base = Widget()
        base.add_widget(ScreenSaver())
        return base
  ScreenSaverApp().run()
