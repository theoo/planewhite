# utils
from kivy.uix.widget import Widget
from kivy.uix.label import Label
import kivy.uix.image


from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.app import App
from kivy.graphics import *
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.core.window import Window

import config

CURSOR_IMG_PATH = "images/cursor.png"

FADE_RAMP = 0.01
FADE_SPEED = 0.01

alpha_fragment = '''
#ifdef GL_ES
    precision highp float;
#endif

/* Outputs from the vertex shader */
varying vec4 frag_color;
varying vec2 tex_coord0;

/* uniform texture samplers */
uniform sampler2D texture0;

/* our custom alpha value */
uniform float alpha;

void main (void){
    vec4 alpha_color = vec4(1, 1, 1, alpha);
    gl_FragColor = alpha_color * frag_color * texture2D(texture0, tex_coord0);
}
'''

class AlphaWidget(Widget):
  alpha = NumericProperty(1.)

  def __init__(self, **kwargs):
    self.canvas = RenderContext()
    self.canvas.shader.fs = alpha_fragment
    super(AlphaWidget, self).__init__(**kwargs)
    Clock.schedule_once(self.init_shader, 0)

  def init_shader(self, dt):
    self.canvas['projection_mat'] = Window.render_context['projection_mat']

  def on_alpha(self, instance, value):
    self.canvas['alpha'] = value

  def pulse_widget_alpha(self, dt):
    from math import cos
    self.alpha = abs(cos(Clock.get_boottime()))

  def fadeIn(self, dt=0):
    self.alpha += FADE_RAMP
    if self.alpha < 1.0:
      Clock.schedule_once(self.fadeIn, FADE_SPEED)
    else:
      print "Reached full opacity"
        

  def fadeOut(self, dt=0):
    self.alpha -= FADE_RAMP
    if self.alpha > 0.0:
      Clock.schedule_once(self.fadeIn, FADE_SPEED)
    else:
      print "Reached full transparency"

      
  def update_shader(self):
    self.alpha = 0.99
    

########################################################################
class ZoneOfDescription(Widget):

  def __init__(self, img=None, pos=(0,0), **kwargs):
    super(ZoneOfDescription, self).__init__(**kwargs)
    
    self.pos = pos
    self.img = img
    self.object = Rectangle(texture=self.img.texture, size=self.img.size)
    self.object.pos = self.pos

    self.color = Color(1,1,1,1) 
    self.canvas.add(self.color)
    self.canvas.add(self.object)
    
    self.size = img.size
    

class ZoneOfInterest(AlphaWidget):

  def __init__(self, img=None, pos=(0,0), **kwargs):
    super(ZoneOfInterest, self).__init__(**kwargs)
    
    self.pos = pos
    self.img = img
    self.object = Rectangle(texture=self.img.texture, size=self.img.size)
    self.object.pos = self.pos
    self.viewed = False # toggled once widget is viewed

    # I store the color to be able to remove it from canvas afterwards.
    self.color = Color(1,1,1,1) 
    self.canvas.add(self.color)
    self.canvas.add(self.object)
    
    # TODO:  this extend the touch area (collision) to the size of image. 
    # If image isn't square the whole widget is touch-able.
    self.size = img.size
    

class Cursor(Widget):
  def __init__(self, **kwargs):
    super(Cursor, self).__init__(**kwargs)
    
    self.cursor = kivy.uix.image.Image(source=config.CURSOR_IMG_PATH, color=(1,1,1,1))
    self.cursor_width = 250
    self.cursor_height = 250

  def on_touch_down(self, touch):
#    self.cursor.size= (self.cursor_height * touch.shape.height, self.cursor_width * touch.shape.width)
    self.cursor.pos = (touch.x - self.cursor.height / 2, touch.y - self.cursor.width / 2)
    self.add_widget(self.cursor)


  def on_touch_move(self, touch):
#    self.cursor.size= (self.cursor_height * touch.shape.height, self.cursor_width * touch.shape.width)    
    self.cursor.pos = (touch.x - self.cursor.height / 2, touch.y - self.cursor.width / 2)

  def on_touch_up(self, touch):
    self.remove_widget(self.cursor)



