# utils
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.image import Image


from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.app import App
from kivy.graphics import *
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.core.window import Window

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
class ZoneOfInterest(AlphaWidget):
  
  def __init__(self, img=None, pos=(0,0), desc="", desc_pos=(0,0), **kwargs):
    super(ZoneOfInterest, self).__init__(**kwargs)
    
    self.pos = pos
    self.img = img
    self.object = Rectangle(texture=self.img.texture, size=self.img.size)
    self.object.pos = self.pos
    self.viewed = False # toggled once widget is viewed
    self.desc = desc
    self.desc_pos = desc_pos

    # I store the color to be able to remove it from canvas afterwards.
    self.color = Color(1,1,1,1) 
    self.canvas.add(self.color)
    self.canvas.add(self.object)
    
    # TODO:  this extend the touch area (collision) to the size of image. 
    # If image isn't square the whole widget is touch-able.
    self.size = img.size
    
    box_size = (450,150)
    box_position = self.desc_pos

    desc_box = Widget()
    
    label = Label( text=self.desc, 
                   font_size=15,
                   font_name="fonts/Akkurat.ttf",
                   size=box_size,
                   pos=box_position,
                   color=(0,0,0,1))
      
    desc_box.add_widget(label)

    self.desc_box = desc_box

