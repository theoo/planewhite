
def set_kwargs(self, **kwargs):
  if kwargs.has_key("controller"):
    self.controller = kwargs.pop("controller")
    self.clientIdIndex = int(self.controller.clientId) - 1
  else:
    self.clientIdIndex = 0

  if kwargs.has_key("modeId"):
    self.modeId = kwargs.pop("modeId")