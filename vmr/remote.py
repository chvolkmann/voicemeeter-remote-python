import ctypes as ct
import time

from .driver import dll
from .errors import VMRError, VMRDriverError
from .input import InputStrip
from .output import OutputBus


class VMRemote:
  def __init__(self):
    self.cache = {}

  def _call(self, fn, *args, check=True, expected=(0,)):
    fn_name = 'VBVMR_' + fn
    retval = getattr(dll, fn_name)(*args)
    if check and retval not in expected:
      raise VMRDriverError(fn_name, retval)
    time.sleep(.1)
    return retval

  def _login(self):
    self._call('Login')
    time.sleep(.3)
  def _logout(self):
    self._call('Logout')
  
  @property
  def type(self):
    buf = ct.c_long()
    self._call('GetVoicemeeterType', ct.byref(buf))
    val = buf.value
    if val == 1:
      return 'Voicemeeter'
    elif val == 2:
      return 'Voicemeeter Banana'
    elif val == 3:
      return 'Voicemeeter Potato'
    else:
      raise VMRError(f'Unexpected VM type: {val}')

  @property
  def version(self):
    buf = ct.c_long()
    self._call('GetVoicemeeterVersion', ct.byref(buf))
    v1 = (buf.value & 0xFF000000) >> 24
    v2 = (buf.value & 0x00FF0000) >> 16
    v3 = (buf.value & 0x0000FF00) >> 8
    v4 = (buf.value & 0x000000FF)
    return (v1, v2, v3, v4)

  @property
  def dirty(self):
    val = self._call('IsParametersDirty', expected=(0,1))
    return (val == 1)
  
  def get(self, param, string=False):
    param = param.encode('ascii')
    if not self.dirty:
      if param in self.cache:
        return self.cache[param]

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
    param = param.encode('ascii')
    if isinstance(val, str):
      if len(val) >= 512:
        raise VMRError('String is too long')
      self._call('SetParameterStringW', param, ct.c_wchar_p(val))
    else:
      self._call('SetParameterFloat', param, ct.c_float(float(val)))
      

  def __enter__(self):
    self._login()
    return self
  def __exit__(self, type, value, traceback):
    self._logout()


class VMBasicRemote(VMRemote):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    raise NotImplementedError()

class VMBananaRemote(VMRemote):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.inputs = [InputStrip.make((i < 3), self, i) for i in range(3+2)]
    self.outputs = [OutputBus.make((i < 3), self, i) for i in range(3+2)]

class VMPotatoRemote(VMRemote):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.inputs = [InputStrip.make((i < 5), self, i) for i in range(5+3)]
    self.outputs = [OutputBus.make((i < 5), self, i) for i in range(5+3)]