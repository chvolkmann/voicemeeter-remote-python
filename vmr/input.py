# param_name => is_numeric
from .errors import VMRError

class InputStrip:
  @classmethod
  def make(cls, is_physical, *args, **kwargs):
    IS_cls = PhysicalInputStrip if is_physical else VirtualInputStrip
    return IS_cls(*args, **kwargs)

  def __init__(self, remote, index):
    self._remote = remote
    self.index = index

  @property
  def identifier(self):
    return f'Strip[{self.index}]'
  
  def get(self, param, **kwargs):
    return self._remote.get(f'{self.identifier}.{param}', **kwargs)
  
  @property
  def solo(self):
    return (self.get('Solo') == 1)
  @property
  def mute(self):
    return (self.get('Mute') == 1)
  
  @property
  def gain(self):
    val = self.get('Gain')
    return (val+60)/60
  @property
  def comp(self):
    return self.get('Comp') / 10
  @property
  def gate(self):
    return self.get('Gate') / 10
  
  @property
  def label(self):
    return self.get('Label', string=True)
  
class PhysicalInputStrip(InputStrip):
  @property
  def mono(self):
    return (self.get('Mono') == 1)
  
  @property
  def device_name(self):
    return self.get('device', string=True)

class VirtualInputStrip(InputStrip):
  @property
  def mc(self):
    return (self.get('Mono') == 1)