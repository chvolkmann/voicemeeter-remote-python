import ctypes as ct
import time
import abc

from .driver import dll
from .errors import VMRError, VMRDriverError
from .input import InputStrip
from .output import OutputBus
from . import kinds
from . import profiles
from .util import merge_dicts

loggedIn = False

class VMRemote(abc.ABC):
  """ Wrapper around Voicemeeter Remote's C API. """
  def __init__(self, delay=.015):
    self.delay = delay
    self.cache = {}

  def _call(self, fn, *args, check=True, expected=(0,)):
    """
    Runs a C API function.
    
    Raises an exception when check is True and the
    function's return value is not 0 (OK).
    """
    fn_name = 'VBVMR_' + fn
    retval = getattr(dll, fn_name)(*args)
    if check and retval not in expected:
      raise VMRDriverError(fn_name, retval)
    time.sleep(self.delay)
    return retval

  def _login(self):
    global loggedIn
    if(loggedIn == False):
      self._call('Login')
      loggedIn = True
  def _logout(self):
    self._call('Logout')
    
  def logout(self):
    self._logout()


  @property
  def type(self):
    """ Returns the type of Voicemeeter installation (basic, banana, potato). """
    buf = ct.c_long()
    self._call('GetVoicemeeterType', ct.byref(buf))
    val = buf.value
    if val == 1:
      return 'basic'
    elif val == 2:
      return 'banana'
    elif val == 3:
      return 'potato'
    else:
      raise VMRError(f'Unexpected Voicemeeter type: {val}')

  @property
  def version(self):
    """ Returns Voicemeeter's version as a tuple (v1, v2, v3, v4) """
    buf = ct.c_long()
    self._call('GetVoicemeeterVersion', ct.byref(buf))
    v1 = (buf.value & 0xFF000000) >> 24
    v2 = (buf.value & 0x00FF0000) >> 16
    v3 = (buf.value & 0x0000FF00) >> 8
    v4 = (buf.value & 0x000000FF)
    return (v1, v2, v3, v4)

  @property
  def dirty(self):
    """ True iff UI parameters have been updated. """
    val = self._call('IsParametersDirty', expected=(0,1))
    return (val == 1)
  
  def get(self, param, string=False):
    """ Retrieves a parameter. """
    param = param.encode('ascii')
    if not self.dirty:
      if param in self.cache:
        pass
        #return self.cache[param]

    if string:
      buf = (ct.c_wchar * 512)()
      self._call('GetParameterStringW', param, ct.byref(buf))
    else:
      buf = ct.c_float()
      self._call('GetParameterFloat', param, ct.byref(buf))
    val = buf.value
    self.cache[param] = val
    return val
  
  def set(self, param, val):
    """ Updates a parameter. """
    param = param.encode('ascii')
    if isinstance(val, str):
      if len(val) >= 512:
        raise VMRError('String is too long')
      self._call('SetParameterStringW', param, ct.c_wchar_p(val))
    else:
      self._call('SetParameterFloat', param, ct.c_float(float(val)))

  def show(self):
    """ Shows Voicemeeter if it's hidden. """
    self.set('Command.Show', 1)
  def shutdown(self):
    """ Closes Voicemeeter. """
    self.set('Command.Shutdown', 1)
  def restart(self):
    """ Restarts Voicemeeter's audio engine. """
    self.set('Command.Restart', 1)

  def apply(self, mapping):
    """ Sets all parameters of a dict. """
    for key, submapping in mapping.items():
      strip, index = key.split('-')
      index = int(index)
      if strip in ('in', 'input'):
        target = self.inputs[index]
      elif strip in ('out', 'output'):
        target = self.outputs[index]
      else:
        raise ValueError(strip)
      target.apply(submapping)
  
  def apply_profile(self, name):
    try:
      profile = self.profiles[name]
      if 'extends' in profile:
        base = self.profiles[profile['extends']]
        profile = merge_dicts(base, profile)
        del profile['extends']
      self.apply(profile)
    except KeyError:
      raise VMRError(f'Unknown profile: {self.kind.id}/{name}')

  def button_setStatus(self, nuLogical, state, mode=2):
    c_nuLogical = ct.c_long(nuLogical)
    c_state = ct.c_float(state)
    c_mode = ct.c_long(mode)
    
    self._call('MacroButton_SetStatus', c_nuLogical, c_state, c_mode)
    
  def button_getStatus(self, nuLogical, mode=2):
    c_nuLogical = ct.c_long(nuLogical)
    c_state = ct.c_float(0)
    c_mode = ct.c_long(mode)
    
    retval = self._call('MacroButton_GetStatus', c_nuLogical, ct.byref(c_state), c_mode)
    return int(c_state.value)
    
  def button_state(self, nuLogical, state):
    mode = 1
    self.button_setStatus(nuLogical, state, mode)
    
  def button_stateOnly(self, nuLogical, state):
    mode = 2
    self.button_setStatus(nuLogical, state, mode)
    
  def button_trigger(self, nuLogical, state):
    mode = 3
    self.button_setStatus(nuLogical, state, mode)
    
  def show_VBANchat(self, state):
    if state not in range(2):
        raise VMRError('State must be 0 or 1')
    self.show()
    self.set('Command.DialogShow.VBANCHAT', state)

 
  def recorder_play(self , state:int=1):
    self.set('recorder.play', state)
   
  def recorder_stop(self, state:int=1):
    self.set('recorder.stop', state)
     
  def recorder_pause(self , state:int=1):
    self.set('recorder.pause', state)
     
  def recorder_replay(self , state:int=1):
    self.set('recorder.replay', state)
     
  def recorder_record(self , state:int=1):
    self.set('recorder.record', state)
     
  def recorder_loop(self, state:int=1):
    self.set('Recorder.mode.Loop', state)
    
  def recorder_ff(self, state:int=1):
    self.set('recorder.ff', state)
    
  def recorder_rw(self, state:int=1):
    self.set('recorder.rew', state)
    
  def recorder(self, action, state:int=1):
    method = 'self.recorder_' + action  
    if state not in range(2):
        raise VMRError('State must be 0 or 1')
        
    try:
      eval(method)(state)
    except AttributeError:
      raise VMRError('Recorder function not supported')
      
  def recorderS_out(self, bus:str, state:int):
    bus_type, number = bus.split('-')
    num_physical, num_virtual = self.kind[2]
    
    if bus_type == 'A' and int(number) in range(num_physical):
      target = 'recorder.A'  + str(number)
    elif bus_type == 'B' and int(number) in range(num_virtual):
      target = 'recorder.B'  + str(number)      
    else:
      raise VMRError('Strip/Bus out of range')

    self.set(target, state)

  def recorderS_load(self, file):
    try:
      self.set('Recorder.load', file)
    except UnicodeError:
      raise VMRError('File full directory must be a raw string')


  def reset(self):
    self.apply_profile('base')

  def __enter__(self):
    self._login()
    return self
  def __exit__(self, type, value, traceback):
    pass


def _make_remote(kind):
  """
  Creates a new remote class and sets its number of inputs
  and outputs for a VM kind.
  
  The returned class will subclass VMRemote.
  """
  def init(self, *args, **kwargs):
    VMRemote.__init__(self, *args, **kwargs)
    self.kind = kind
    self.num_A, self.num_B = kind.layout
    self.inputs = tuple(InputStrip.make((i < self.num_A), self, i) for i in range(self.num_A+self.num_B))
    self.outputs = tuple(OutputBus.make((i < self.num_B), self, i) for i in range(self.num_A+self.num_B))
  def get_profiles(self):
    return profiles.profiles[kind.id]
 
  return type(f'VMRemote{kind.name}', (VMRemote,), {
    '__init__': init,
    'profiles': property(get_profiles)
  })

_remotes = {kind.id: _make_remote(kind) for kind in kinds.all}

def connect(kind_id, delay=None):
  if delay is None:
    delay = .015
  """ Connect to Voicemeeter and sets its strip layout. """
  try:
    cls = _remotes[kind_id]
    return cls(delay=delay)
  except KeyError as err:
    raise VMRError(f'Invalid Voicemeeter kind: {kind_id}')
