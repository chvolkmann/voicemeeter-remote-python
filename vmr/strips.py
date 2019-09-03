# param_name => is_numeric
from .errors import VMRError
from functools import wraps

INPUT_PARAM_MAP = {
  'Mono': True,
  'Mute': True,
  'Solo': True,
  'MC': True,
  'Gain': True,
  'Comp': False,
  'Gate': False
}

def _bool_param(param):
  @wraps
  def get_param(self):
    return (self.get(param) == 1)
  return get_param

class InputStrip:
  def __init__(self, remote, index, is_virtual):
    self._remote = remote
    self.index = index
    self.is_virtual = is_virtual

  @property
  def name(self):
    return f'Strip[{self.index}]'
  
  def get(self, param):
    if not param in INPUT_PARAM_MAP:
      raise VMRError(f'Invalid InputStrip parameter: {param}')
    return self._remote.get(f'{self.name}.{param}', numeric=INPUT_PARAM_MAP[param])
  
  @property
  def mono(self):
    if self.is_virtual:
      raise VMRError('Mono is not supported on virtual InputStrips')
    return (self.get('Mono') == 1)
  @property
  def mc(self):
    if not self.is_virtual:
      raise VMRError('M.C. is not supported on physical InputStrips')
    return (self.get('Mono') == 1)
  @property
  def solo(self):
    return (self.get('Solo') == 1)
  @property
  def mute(self):
    return (self.get('Mute') == 1)