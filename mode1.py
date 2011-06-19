# ScreenSaver

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.app import App

from kivy.clock import Clock
from kivy.animation import Animation

from kivy.uix.boxlayout import BoxLayout

import kivy.core.image
import kivy.uix.image

from kivy.graphics import *

from lib.utils import ZoneOfInterest
import lib.config, lib.kwargs

# Configuration
SCAN_IMG_PATH = 'images/scan.png'
SCAN_DURATION = 2.0
NETWORK_DELAY = 0 # frames
TRIGGER_POINTS_THRESHOLD = 100


########################################################################
class ScreenSaver(Widget):
  
  def __init__(self, **kwargs):

    lib.kwargs.set_kwargs(self, **kwargs)

    super(ScreenSaver, self).__init__(**kwargs)  
    
    self.pos = (lib.config.viewport[self.clientIdIndex][0], 0)
    self.width = abs(lib.config.viewport[self.clientIdIndex][0] - lib.config.viewport[self.clientIdIndex][1])

    self.scan_duration = SCAN_DURATION / Window.width * (self.width)

    self.points = []
    self.trigger_points = []
    
    # ZoneOfInterest
    self.shapes = []
    
    for zi in lib.config.zones_of_interest[self.clientIdIndex]:
      self.shapes.append( ZoneOfInterest( img=kivy.core.image.Image(zi[0]),
                                          pos=zi[1],
                                          alpha_index=1.0) )

    # Scaner
    self.scan_endMessageSent = False
    self.screensaver_touchedMessageSent = False
      
    self.img = kivy.uix.image.Image(source=SCAN_IMG_PATH, size=(218,768), color=[1,1,1,0.5], pos=(0 - 218,0))
    self.add_widget(self.img)
    
    # cartel
    if self.clientId == 1
      self.cartel = Label(text="PlaneWhite", pos=(600,700), font_size=40)
      self.add_widget = self.cartel
    

# basis
  def start(self):
    # start is called on each scan, not only when changin mode.
    print "ScreenSaver start() called"
    self.scan_endMessageSent = False
    Clock.schedule_once(self.scan, 0)


  def stop(self):
    print "ScreenSaver stop() called"
    self.reset()
    Clock.unschedule(self.scan)
    
    
  def reset(self):
    self.screensaver_touchedMessageSent = False    
    self.points = []
    self.trigger_points = []

    self.remove_widget(self.img)    
    self.canvas.clear()
    self.add_widget(self.img)
    

# Custom methods
  def scan(self, dt):
    self.img.pos = (self.pos[0] - self.img.width,0)
    
    a1 = Animation(pos=(self.pos[0] + self.width, 0), duration=self.scan_duration)
    a1.bind(on_progress=self.syncServerCommunication)
#    a1.bind(on_complete=self.onAnimComplete)
    a1.start(self.img)


  def draw_ellipse(self, touch):
    # Use this instead of "append" if you are displaying Point cloud.
    # self.points += touch.pos
    self.points.append(touch.pos)

    self.remove_widget(self.img)

    self.canvas.clear()
       
    with self.canvas:
      StencilPush()
      
      for pos in self.points:
        diameter = 100
        Ellipse(pos=(pos[0] - diameter / 2, pos[1] - diameter / 2), size=(diameter, diameter))
      
      StencilUse()      
      for shape in self.shapes:
        shape.object
        Rectangle(texture=shape.img.texture, size=shape.img.size, pos=shape.pos)
      
      StencilPop()

    self.add_widget(self.img)


  def add_trigger_point(self, touch):
    for shape in self.shapes:
      if shape.collide_point(*touch.pos):
        self.trigger_points.append(touch.pos)


# Custom Callbacks
  def onAnimComplete(self, animation=False, target=False):
    Clock.schedule_once(self.scan, 0)


  def syncServerCommunication(self, animation, target, progression):
    if target.x >= (self.pos[0] + self.width - target.width - NETWORK_DELAY):
      if not self.scan_endMessageSent:
        print "Scan reached right of screen."
        self.controller.sendMessage("scan_end") # sync next client
        self.scan_endMessageSent = True


# Kivy Callbacks
  def on_touch_down(self, touch):
    self.draw_ellipse(touch)
    self.add_trigger_point(touch)


  def on_touch_move(self, touch):
    self.draw_ellipse(touch)
    self.add_trigger_point(touch)    


  def on_touch_up(self, touch):
    if len(self.trigger_points) > TRIGGER_POINTS_THRESHOLD:
      if not self.screensaver_touchedMessageSent:
        print "Screensaver touched. ", len(self.trigger_points)
        self.controller.sendMessage("screensaver_touched") # go to next mode
        self.screensaver_touchedMessageSent = True



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
