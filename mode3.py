# Discovering

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.app import App

from kivy.clock import Clock
from kivy.animation import Animation

from kivy.uix.stencilview import StencilView
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button

from kivy.core.image import Image
from kivy.core.text import LabelBase
from kivy.graphics import *

import lib.config, lib.kwargs

# Configuration

########################################################################
class ZoneOfInterest(Widget):
  
  def __init__(self, obj=None, pos=(0,0), desc=None, desc_pos=(0,0), **kwargs):
    super(ZoneOfInterest, self).__init__(**kwargs)

    
    if kwargs.has_key("controller"):
      self.controller = kwargs.pop("controller")
    
    self.alpha_index = 0.0
    self.alpha_direction = 0

    # I store the color to be able to remove it from canvas afterwards.
    self.color = Color(1,1,1,self.alpha_index) 
    self.canvas.add(self.color)
    self.canvas.add(obj)
    

    self.pos = pos
    self.object = obj
    self.object.pos = self.pos
    self.viewed = False # toggled once widget is viewed
    self.desc = desc
    self.desc_pos = desc_pos
    
    # TODO:  this extend the touch area (collision) to the size of image. 
    # If image isn't square the whole widget is touch-able.
    self.size = obj.size
    
    box_size = (450,150)
    box_position = self.desc_pos

    desc_box = Widget()
    
    label = Label( text=self.desc, 
                   font_size=20,
                   size=box_size,
                   pos=box_position,
                   color=(1,1,1,1))
        
    with desc_box.canvas:
      Color(0,0,0,0.5)
      Rectangle(size=box_size, pos=box_position)
      
    desc_box.add_widget(label)

    self.desc_box = desc_box


########################################################################
class Discovering(Widget):

  def __init__(self, **kwargs):

    lib.kwargs.set_kwargs(self, **kwargs)
          
    super(Discovering, self).__init__(**kwargs)

    self.all_zones_of_interest_viewedMessageSent = False

    # First item of self.shapes is the background
    self.bg = Image(lib.config.backgrounds[self.clientIdIndex])
    with self.canvas:
      Rectangle(texture=self.bg.texture, size=self.bg.size, pos=(0,0))

    # zones of interest
    self.shapes = []
    
    for zi in lib.config.zones_of_interest[self.clientIdIndex]:
      img = Image(zi[0])
      self.shapes.append( ZoneOfInterest( obj=Rectangle(texture=img.texture, size=img.size),
                                          pos=zi[1],
                                          desc=zi[2],
                                          desc_pos=zi[3]) )

    Clock.schedule_interval(self.pulse, 0.1)
    
    for shape in self.shapes:            
      # add to the view
      self.add_widget(shape)


# basis
  def start(self):
    pass

    
  def stop(self):
    self.reset()


  def reset(self, instance=False):
    self.all_zones_of_interest_viewedMessageSent = False    
    for shape in self.shapes:
      self.remove_widget(shape.desc_box)
      shape.viewed = False
    
# Custom methods
  def checkIfModeIsCompleted(self, instance=False):
    # exits if not all shapes are viewed
    for shape in self.shapes:
      if not shape.viewed:
        return
    
    if not self.all_zones_of_interest_viewedMessageSent:
      print "All zones of interest seens"
      self.controller.sendMessage("all_zones_of_interest_viewed") # go to next mode
      self.all_zones_of_interest_viewedMessageSent = True


  def pulse(self, dt):
    for shape in self.shapes:
      # TODO: improve!
      if shape.alpha_direction == 0:
        if shape.alpha_index < 1.0:
          shape.alpha_index += 0.1
        else:
          shape.alpha_direction = 1
      else:
        if shape.alpha_index > 0.1:
          shape.alpha_index -= 0.1
        else:
          shape.alpha_direction = 0

      shape.canvas.remove(shape.color)
      shape.color = Color(1,1,1,shape.alpha_index)
      shape.canvas.insert(0, shape.color )


# Custom callbacks


# Kivy callbacks
  def on_touch_down(self, touch):
    pass

     
  def on_touch_move(self, touch):
    pass

    
  def on_touch_up(self, touch):
    # check if mode is complete before so I can read the text.
    # Next touch will throw a message to the server
    self.checkIfModeIsCompleted()

    for shape in self.shapes:
      # add interaction
      if shape.collide_point(*touch.pos):
        if self.children.count(shape.desc_box) < 1:
          # displays text box
          # TODO: Clock.unschedule()
          self.add_widget(shape.desc_box)
          shape.viewed = True


########################################################################

      
if __name__ == '__main__':
  class DiscoveringApp(App):
  
    def build(self):
      base = Widget()
      
      discovering = Discovering()
      base.add_widget(discovering)
    
#      clearbtn = Button(text="clear", font_size=14)
#      clearbtn.bind(on_release=discovering.clear)
#      base.add_widget(clearbtn)
      
      return base

  DiscoveringApp().run()
