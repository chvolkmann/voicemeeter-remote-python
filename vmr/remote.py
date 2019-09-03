import ctypes as ct
import time

from .driver import dll
from .errors import VMRError, VMRDriverError
from .strips import InputStrip


class VMRemote:
  @classmethod
  def make(cls, version, *args, **kwargs):
    if version == 1:
      return VMBasicRemote(*args, **kwargs)
    elif version in (2, 'banana'):
      return VMBananaRemote(*args, **kwargs)
    elif version in (3, 'potato'):
      return VMPotatoRemote(*args, **kwargs)
    else:
      raise VMRError(f'Invalid Voicemeeter version: {version}')

  def _call(self, fn, *args, throw=True, expected=(0,)):
    fn_name = 'VBVMR_' + fn
    retval = getattr(dll, fn_name)(*args)
    if throw and retval not in expected:
      raise VMRDriverError(fn_name, retval)
    time.sleep(.5)
    return retval

  def _login(self):
    self._call('Login')
    time.sleep(.5)
    self.dirty
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
  
  def get(self, param, numeric=True):
    print(f'GET {param}')
    param = param.encode('ascii')
    if numeric:
      buf = ct.c_float()
      self._call('GetParameterFloat', param, ct.byref(buf))
      return buf.value

    else:
      raise NotImplementedError()

  def __enter__(self):
    self._login()
    return self
  def __exit__(self, type, value, traceback):
    self._logout()


class VMBasicRemote(VMRemote):
  pass

class VMBananaRemote(VMRemote):
  pass

class VMPotatoRemote(VMRemote):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    self.inputs = [InputStrip(self, i, is_virtual=(i >= 5)) for i in range(8)]