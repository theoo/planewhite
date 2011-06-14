  def draw_ellipse(self, touch):
#    self.points.append(touch.pos)

    self.canvas.clear()
       
    with self.canvas:
      StencilPush()
      # Point(pointsize=20., points=self.points)
      
      Ellipse(pos=touch.pos, size=(50,50))
      
      StencilUse()
      Image(source="../images/kand8_1.jpg", size=(1024,768), color=[1,1,1,1], pos=(0,0))
      
      StencilPop() 