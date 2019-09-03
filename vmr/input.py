# param_name => is_numeric
from .errors import VMRError
from .util import VMElement, bool_prop, str_prop, float_prop

class InputStrip(VMElement):
  @classmethod
  def make(cls, is_physical, *args, **kwargs):
    IS_cls = PhysicalInputStrip if is_physical else VirtualInputStrip
    return IS_cls(*args, **kwargs)

  @property
  def identifier(self):
    return f'Strip[{self.index}]'
  
  solo = bool_prop('Solo')
  mute = bool_prop('Mute')
  
  gain = float_prop('Gain', range=(-60,12))
  comp = float_prop('Comp', range=(0,10))
  gate = float_prop('Gate', range=(0,10))

  label = str_prop('Label')
  
class PhysicalInputStrip(InputStrip):
  mono = bool_prop('Mono')

class VirtualInputStrip(InputStrip):
  mc = bool_prop('MC')