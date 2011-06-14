
from kivy.app import App
from controller import Controller


class PlaneWhiteApp(App):
  def build(self):
    self.controller = Controller()
    return self.controller


  def on_stop(self):
    self.controller.cleanupOnExit()
    print "onClose"

PlaneWhiteApp().run()
