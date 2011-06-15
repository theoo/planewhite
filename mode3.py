# ScreenSaver

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.app import App

from kivy.clock import Clock
from kivy.animation import Animation

from kivy.uix.stencilview import StencilView
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from kivy.core.image import Image
from kivy.graphics import *

# Configuration
BACKGROUND = "images/bgs/2.jpg"
CUT = ( "images/cut/2_258x574.png", (258, 768 - 574) )


class ZoneOfInterest(Widget):
  def __init__(self, obj=None, desc=None, pos=(0,0), **kwargs):
    super(ZoneOfInterest, self).__init__(**kwargs)

    self.alpha_index = 0.0
    self.alpha_direction = 0

    # I store the color to be able to remove it from canvas afterwards.
    self.color = Color(1,1,1,self.alpha_index) 
    self.canvas.add(self.color)
    self.canvas.add(obj)
    
    self.object = obj
    self.desc = desc
    self.pos = pos

    desc_box = BoxLayout(size=(300,300))
    content = Label(text=self.desc, font_size=20, color=(0,0,0,1))
    desc_box.add_widget(content)
    self.desc_box = desc_box
    
    self.object.pos = self.pos


class Discovering(Widget):

  def __init__(self, **kwargs):
    super(Discovering, self).__init__(**kwargs)
      
    # First item of self.shapes is the background
    bg = Image(BACKGROUND)    
    with self.canvas:
      Rectangle(texture=bg.texture, size=bg.size, pos=(0,0))

    # zones of interest
    self.shapes = []

    img = Image(CUT[0])
    self.shapes.append( ZoneOfInterest( Rectangle(texture=img.texture, size=img.size),
                                        "This is a wonderful demonstration of ten words for carina's sake.",
                                        CUT[1] ) )

    Clock.schedule_interval(self.pulse, 0.1)
    
    for shape in self.shapes:            
      # add to the view
      self.add_widget(shape)



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

      
  def on_touch_down(self, touch):
    for shape in self.shapes:
      # add interaction
      if shape.collide_point(*touch.pos):
        if self.children.count(shape.desc_box) < 1:
          self.add_widget(shape.desc_box)        
        
  def on_touch_move(self, touch):
    pass
    
  def on_touch_up(self, touch):
    pass
    
      
class DiscoveringApp(App):
    def build(self):
      base = Widget()
      base.add_widget(Discovering())
      
      return base
      
if __name__ == '__main__':
    DiscoveringApp().run()
