from os import path
import sys
import platform
import ctypes

from .errors import VMRError

bits = 64 if sys.maxsize > 2**32 else 32
os = platform.system()

if os != 'Windows' or bits != 64:
  raise VMRError('The vmr package only supports Windows 64-bit')


DLL_NAME = 'VoicemeeterRemote64.dll'

vm_base = path.join(path.expandvars('%ProgramFiles(x86)%'), 'VB', 'Voicemeeter')

def vm_subpath(*fragments):
  """ Returns a path based from Voicemeeter's install directory. """
  return path.join(vm_base, *fragments)

dll_path = vm_subpath(DLL_NAME)

if not path.exists(dll_path):
  raise VMRError(f'Could not find {DLL_NAME}')

dll = ctypes.cdll.LoadLibrary(dll_path)