# utils
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.app import App

from kivy.uix.label import Label
from kivy.core.image import Image

from kivy.graphics import *

########################################################################
class ZoneOfInterest(Widget):
  
  def __init__(self, img=None, pos=(0,0), desc="", desc_pos=(0,0), alpha_index=0.0, **kwargs):
    super(ZoneOfInterest, self).__init__(**kwargs)
    
    self.alpha_index = alpha_index
    self.alpha_direction = 0

    self.pos = pos
    self.img = img
    self.object = Rectangle(texture=self.img.texture, size=self.img.size)
    self.object.pos = self.pos
    self.viewed = False # toggled once widget is viewed
    self.desc = desc
    self.desc_pos = desc_pos

    # I store the color to be able to remove it from canvas afterwards.
    self.color = Color(1,1,1,self.alpha_index) 
    self.canvas.add(self.color)
    self.canvas.add(self.object)
    
    # TODO:  this extend the touch area (collision) to the size of image. 
    # If image isn't square the whole widget is touch-able.
    self.size = img.size
    
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
