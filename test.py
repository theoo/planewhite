from kivy.uix.widget import Widget
from kivy.uix.label import Label

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.app import App
from kivy.graphics import *
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.core.window import Window

import kivy.core.image

from lib.utils import ZoneOfInterest
import lib.config, lib.kwargs


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

        
class ShaderAlphaApp(App):
    def build(self):
        fade = AlphaWidget()
        child = ZoneOfInterest( img=kivy.core.image.Image("images/cut/2a_187x607.png"),
                                          pos=(10,10),
                                          alpha_index=1.0)
                                          
        fade.add_widget(child)

        # a little clock to change the alpha of the scatter 
        Clock.schedule_interval(self.change_scatter_alpha, 1 / 30)
        return fade
        

    def change_scatter_alpha(self, dt):
        from math import cos
        self.root.alpha = abs(cos(Clock.get_boottime()))

ShaderAlphaApp().run()        