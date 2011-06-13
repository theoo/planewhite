# Main program

from mode1 import ScreenSaver

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.app import App


class PlaneWhite(App):

  def build(self):
    base = Widget()
    
    ss = ScreenSaver()
    base.add_widget(ss)
    
    return base

if __name__ == '__main__':
    PlaneWhite().run()