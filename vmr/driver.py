import os
import shutil
import ctypes

from .util import project_path
from .errors import VMRError

VM_BASE_PATH = os.path.join(os.path.expandvars('%ProgramFiles(x86)%'), 'VB', 'Voicemeeter')
def vm_path(*fragments):
  return os.path.join(VM_BASE_PATH, *fragments)

dll_src = vm_path('VoicemeeterRemote64.dll')
dll_dst = project_path('vendor', 'VoicemeeterRemote64.dll')
if not os.path.exists(project_path('vendor', 'VoicemeeterRemote64.dll')):
  shutil.copy(dll_src, dll_dst)


dll = ctypes.cdll.LoadLibrary(dll_dst)