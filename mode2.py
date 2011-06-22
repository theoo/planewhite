# Learning

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.app import App

from kivy.animation import Animation

from kivy.uix.boxlayout import BoxLayout
import kivy.core.image
import kivy.uix.image
#from kivy.core.image import Image

from kivy.graphics import *

from lib.utils import ZoneOfInterest, AlphaWidget
import lib.config, lib.kwargs

# Configuration
MAX_POINTS = 400 # max points to discover the background
RATIO = 0.8 # ratio of theses points to reach the next mode

########################################################################
class Learning(Widget):
  
  def __init__(self, **kwargs):

    lib.kwargs.set_kwargs(self, **kwargs)
    
    super(Learning, self).__init__(**kwargs)  
          
    # Widget position
    self.pos = (lib.config.viewport[self.clientIdIndex][0], 0)
    self.width = lib.config.viewport[self.clientIdIndex][1]
    self.background_path = "images/bgs/" + str(self.clientIdIndex + 1) + ".jpg"
    
    self.threshold_reachedMessageSent = False

    self.points = []
    
    # ZoneOfInterest
    self.shapes = []
    
    for zi in lib.config.zones_of_interest[self.clientIdIndex]:
      self.shapes.append( ZoneOfInterest( img=kivy.core.image.Image(zi[0]),
                                          pos=zi[1],
                                          alpha_index=1.0) )

    
    rez = lib.config.viewport[self.clientIdIndex]
    self.max_points = (MAX_POINTS * RATIO / 1024) * abs(rez[0] - rez[1])


# basis
  def start(self):
    print "Learning start() called"
    self.add_shapes()
    
    
  def stop(self):
    print "Learning stop() called"
    self.reset()


  def fadein(self):
    pass


  def fadeout(self):
    pass    
        

  def reset(self):
    self.threshold_reachedMessageSent = False
    self.points = []
    self.canvas.clear()


# Custom methods
  def checkIfModeIsCompleted(self):
    if len(self.points) >= self.max_points:
      if not self.threshold_reachedMessageSent:
        print "Max point reached with ", str(len(self.points))
        # self.reset() # should be resetted when server send top command
        self.controller.sendMessage("threshold_reached") # go to next mode
        self.threshold_reachedMessageSent = True
      

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
      kivy.uix.image.Image(source=self.background_path, size=(1024,768), color=[1,1,1,1], pos=(0,0))
      
      StencilPop()

    self.add_shapes()

    
  def add_shapes(self):
    for shape in self.shapes:
      self.canvas.add(shape.object)
        
# Custom Callbacks

# Kivy Callbacks    
  def on_touch_down(self, touch):
    self.draw_ellipse(touch)
    

  def on_touch_move(self, touch):
    self.draw_ellipse(touch)       


  def on_touch_up(self, touch):    
    self.checkIfModeIsCompleted()    


########################################################################

      
if __name__ == '__main__':
  class LearningApp(App):
    def build(self):      
      base = Widget()
      learn = Learning()
      base.add_widget(learn)
      learn.start()
      return base

  LearningApp().run()
