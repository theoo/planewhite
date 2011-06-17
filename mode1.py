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
SCAN_DURATION = 2.0
NETWORK_DELAY = 0 # frames


########################################################################
class ScreenSaver(Widget):
  
  def __init__(self, **kwargs):
    super(ScreenSaver, self).__init__(**kwargs)  

    if kwargs.has_key("controller"):
      self.controller = kwargs.pop("controller")

    if kwargs.has_key("modeId"):
      self.modeId = kwargs.pop("modeId") 
    
    self.scan_endMessageSent = False
      
    self.img = Image(source=SCAN_IMG_PATH, size=(218,768), color=[1,1,1,0.5], pos=(0,0))
    self.add_widget(self.img)



# basis
  def start(self):
    print "start called on ScreenSaver"
    Clock.schedule_once(self.scan, 0)


  def stop(self):
    self.reset()
    
    
  def reset(self):
    self.scan_endMessageSent = False


# Custom methods
  def scan(self, dt):
    self.img.pos = (-self.img.width,0)
    a1 = Animation(pos=(Window.width, 0), duration=SCAN_DURATION)
    a1.bind(on_progress=self.syncServerCommunication)
    a1.start(self.img)
    a1.bind(on_complete=self.onAnimComplete)

# Custom Callbacks
  def onAnimComplete(self, animation=False, target=False):
    self.reset()
    

  def syncServerCommunication(self, animation, target, progression):
    if target.x >= (1024 - target.width - NETWORK_DELAY):
      if not self.scan_endMessageSent:
        print "Scan reached right of screen."
        self.controller.sendMessage("scan_end") # sync next client
        self.scan_endMessageSent = True


# Kivy Callbacks
  def on_touch_down(self, touch):
    print "Screensaver touched."
    self.controller.sendMessage("screensaver_touched") # go to next mode


########################################################################      
if __name__ == '__main__':
  class ScreenSaverApp(App):
      def build(self):
        base = Widget()
        ss = ScreenSaver()
        ss.start()
        base.add_widget(ss)
        
        return base
  ScreenSaverApp().run()
