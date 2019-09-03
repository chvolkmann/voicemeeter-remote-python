from .errors import VMRError
from .strip import VMElement, bool_prop, str_prop, float_prop

class InputStrip(VMElement):
  @classmethod
  def make(cls, is_physical, version, remote, index, **kwargs):
    if version == 'banana':
      IS_cls = PhysicalInputStripBanana if is_physical else VirtualInputStripBanana
    elif version == 'potato':
      IS_cls = PhysicalInputStripPotato if is_physical else VirtualInputStripPotato
    else:
      raise NotImplementedError()
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
  
class PhysicalInputStrip(InputStrip):
  mono = bool_prop('Mono')

class VirtualInputStrip(InputStrip):
  mc = bool_prop('MC')

BANANA_LAYOUT = (3, 2)
BananaMixin = type('BananaMixin', (), {
  **{f'A{i}': bool_prop(f'A{i}') for i in range(BANANA_LAYOUT[0])},
  **{f'B{i}': bool_prop(f'B{i}') for i in range(BANANA_LAYOUT[1])}
})

POTATO_LAYOUT = (5, 3)
PotatoMixin = type('PotatoMixin', (), {
  **{f'A{i}': bool_prop(f'A{i}') for i in range(POTATO_LAYOUT[0])},
  **{f'B{i}': bool_prop(f'B{i}') for i in range(POTATO_LAYOUT[1])}
})

PhysicalInputStripBanana = type('PhysicalInputStripBanana', (PhysicalInputStrip, BananaMixin), {})
VirtualInputStripBanana = type('VirtualInputStripBanana', (PhysicalInputStrip, BananaMixin), {})
PhysicalInputStripPotato = type('PhysicalInputStripPotato', (PhysicalInputStrip, PotatoMixin), {})
VirtualInputStripPotato = type('VirtualInputStripPotato', (VirtualInputStrip, PotatoMixin), {})