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

# Configuration
BACKGROUND = "images/bgs/2.jpg"
FADE_IN_SPEED = 0.01
ALPHA_INDEX_STEP = 0.01


########################################################################
class Credits(Widget):
  
  def __init__(self, **kwargs):
    
    if kwargs.has_key("controller"):
      self.controller = kwargs.pop("controller")
    self.modeId = kwargs.pop("modeId") 

    super(Credits, self).__init__(**kwargs)  

    with self.canvas:
      Image(source=BACKGROUND, size=(1024,768), color=(1,1,1,0))

    self.alpha_index = 0.0


# basis
  def start(self):
    self.alpha_index = 0.0
    Clock.schedule_once(self.fadeIn, 0)
    Clock.schedule_once(self.displayCredits, 30) # easter eggs
    Clock.schedule_once(self.announceTheEnd, 60) # restart screensaver
    

  def stop(self):
    pass


# Custom methods
  def fadeIn(self, instance=False):
    self.alpha_index += ALPHA_INDEX_STEP
    
    self.canvas.clear()  
    with self.canvas:
      Image(source=BACKGROUND, size=(1024,768), color=(1,1,1,self.alpha_index))
    
    if self.alpha_index <= 1.0:
      Clock.schedule_once(self.fadeIn,FADE_IN_SPEED)


# Custom callbacks  
  def displayCredits(self, instance=False):
    self.add_widget(Label(text="Credits", font_size=20, color=(1,1,1,1)))


  def announceTheEnd(self, instance=False):
    print "This is the end."
    self.controller.sendMessage("credits_timeout") # go back to mode1, ScreenSaver
    

# Kivy callbacks    
  def on_touch_down(self, touch):
    # Doesn't do anything if touched within the tenth first seconds.
    if Clock.get_boottime() > 10.0:
      print "Credits touched at, ", Clock.get_boottime()
      self.controller.sendMessage("credits_touched") # go back to mode2, Learning 


########################################################################

      
if __name__ == '__main__':
  class CreditsApp(App):
    def build(self):      
      base = Widget()
      base.add_widget(Credits())
      
      return base
      
  CreditsApp().run()
