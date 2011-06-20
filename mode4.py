# Credits
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.app import App

from kivy.clock import Clock, ClockBase
from kivy.animation import Animation

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

from kivy.graphics import *

import lib.config, lib.kwargs

# Configuration
FADE_IN_SPEED = 0.01
ALPHA_INDEX_STEP = 0.01

TOUCH_DELAY = 2.0
CREDIT_DELAY = 5.0
SCREENSAVER_DELAY = 10.0

########################################################################
class Credits(Widget):
  
  def __init__(self, **kwargs):

    lib.kwargs.set_kwargs(self, **kwargs)

    super(Credits, self).__init__(**kwargs)  

    self.credits_touchedMessageSent = False
    self.credits_timeoutMessageSent = False

    self.last_runtime = 0.0

    self.background_path = lib.config.backgrounds[self.clientIdIndex]

    with self.canvas:
      Image(source=self.background_path, size=(1024,768), color=(1,1,1,0))

    self.alpha_index = 0.0


# basis
  def start(self):
    print "Credits start() called"    
    Clock.schedule_once(self.fadeIn, 0)
    if self.clientIdIndex == 2:
      Clock.schedule_once(self.displayCredits, CREDIT_DELAY) # easter eggs
    
    Clock.schedule_once(self.announceTheEnd, SCREENSAVER_DELAY) # restart screensaver
    self.last_runtime = Clock.get_boottime()
    

  def stop(self):
    print "Credits stop() called"    
    self.reset()
    Clock.unschedule(self.fadeIn)
    Clock.unschedule(self.displayCredits)
    Clock.unschedule(self.announceTheEnd)

  def fadein(self):
    pass


  def fadeout(self):
    pass    


  def reset(self):
    self.alpha_index = 0.0    
    self.credits_touchedMessageSent = False
    self.credits_timeoutMessageSent = False

# Custom methods
  def fadeIn(self, instance=False):
    self.alpha_index += ALPHA_INDEX_STEP
    
    self.canvas.clear()  
    with self.canvas:
      Image(source=self.background_path, size=(1024,768), color=(1,1,1,self.alpha_index))
    
    if self.alpha_index <= 1.0:
      Clock.schedule_once(self.fadeIn,FADE_IN_SPEED)


# Custom callbacks  
  def displayCredits(self, instance=False):
      self.add_widget(Label(text="Carina Ow.", font_size=50, color=(1,1,1,1), pos=Window.center))


  def announceTheEnd(self, instance=False):
    if not self.credits_timeoutMessageSent:
      print "This is the end."
      self.controller.sendMessage("credits_timeout") # go back to mode1, ScreenSaver
      self.credits_timeoutMessageSent = True
    

# Kivy callbacks    
  def on_touch_down(self, touch):
    # Doesn't do anything if touched within the tenth first seconds.
    if abs(Clock.get_boottime() - self.last_runtime) > TOUCH_DELAY:
      if not self.credits_touchedMessageSent:
        print "Credits touched at, ", Clock.get_boottime()
        self.controller.sendMessage("credits_touched") # go back to mode2, Learning
        self.credits_touchedMessageSent = True



########################################################################

      
if __name__ == '__main__':
  class CreditsApp(App):
    def build(self):      
      base = Widget()
      base.add_widget(Credits())
      
      return base
      
  CreditsApp().run()
