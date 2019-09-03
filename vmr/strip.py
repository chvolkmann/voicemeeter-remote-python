import abc

class VMElement(abc.ABC):
  def __init__(self, remote, index):
    self._remote = remote
    self.index = index

  def get(self, param, **kwargs):
    return self._remote.get(f'{self.identifier}.{param}', **kwargs)
  def set(self, param, val, **kwargs):
    self._remote.set(f'{self.identifier}.{param}', val, **kwargs)
  
  @abc.abstractmethod
  def identifier(self):
    pass
    

def bool_prop(param):
  def getter(self):
    return (self.get(param) == 1)
  def setter(self, val):
    return self.set(param, 1 if val else 0)
  return property(getter, setter)

def str_prop(param):
  def getter(self):
    return self.get(param, string=True)
  def setter(self, val):
    return self.set(param, val)
  return property(getter, setter)

def float_prop(param, range=None):
  def getter(self):
    val = self.get(param)
    if range:
      lo, hi = range
      val = (val+lo)/(lo+hi)
    return val
  def setter(self, val):
    if range:
      lo, hi = range
      val = val*(lo+hi)-lo
    return self.set(param, val)
  return property(getter, setter)