from .errors import VMRError
from .strip import VMElement, bool_prop, str_prop, float_prop
from . import kinds

class InputStrip(VMElement):
  @classmethod
  def make(cls, is_physical, remote, index, **kwargs):
    PhysStrip, VirtStrip = _strip_pairs[remote.kind.id]
    IS_cls = PhysStrip if is_physical else VirtStrip
    return IS_cls(remote, index, **kwargs)

  def __init__(self, remote, index):
    super().__init__(remote, index)

  @property
  def identifier(self):
    return f'Strip[{self.index}]'
  
  solo = bool_prop('Solo')
  mute = bool_prop('Mute')
  
  gain = float_prop('Gain', range=(-60,12))
  comp = float_prop('Comp', range=(0,10))
  gate = float_prop('Gate', range=(0,10))

  label = str_prop('Label')

  def apply(self, **mapping):
    for key, val in mapping.items():
      setattr(self, key, val)
  
class PhysicalInputStrip(InputStrip):
  mono = bool_prop('Mono')

class VirtualInputStrip(InputStrip):
  mc = bool_prop('MC')


def _make_strip_mixin(kind):
  num_A, num_B = kind.layout
  return type(f'StripMixin{kind.name}', (), {
    **{f'A{i}': bool_prop(f'A{i}') for i in range(1, num_A+1)},
    **{f'B{i}': bool_prop(f'B{i}') for i in range(1, num_B+1)}
  })

_strip_mixins = {kind.id: _make_strip_mixin(kind) for kind in kinds.all}

def _make_strip_pair(kind):
  StripMixin = _strip_mixins[kind.id]
  PhysStrip = type(f'PhysicalInputStrip{kind.name}', (PhysicalInputStrip, StripMixin), {})
  VirtStrip = type(f'VirtualInputStrip{kind.name}', (VirtualInputStrip, StripMixin), {})
  return (PhysStrip, VirtStrip)

_strip_pairs = {kind.id: _make_strip_pair(kind) for kind in kinds.all}