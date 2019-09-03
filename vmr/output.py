# param_name => is_numeric
from .errors import VMRError
from .util import VMElement, bool_prop, str_prop, float_prop

class OutputBus(VMElement):
  @classmethod
  def make(cls, is_physical, *args, **kwargs):
    OB_cls = PhysicalOutputBus if is_physical else VirtualOutputBus
    return OB_cls(*args, **kwargs)

  @property
  def identifier(self):
    return f'Bus[{self.index}]'
  
  mute = bool_prop('Mute')
  gain = float_prop('Gain', range=(-60,12))
  
class PhysicalOutputBus(OutputBus):
  pass

class VirtualOutputBus(OutputBus):
  pass