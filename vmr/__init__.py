import subprocess as sp
import time
from .remote import connect
from .driver import vm_subpath

def open(delay=1):
  sp.Popen([vm_subpath('voicemeeter8.exe')])
  time.sleep(delay)

blank_input = {
  'A1': False,
  'A2': False,
  'A3': False,
  'A4': False,
  'A5': False,
  'B1': False,
  'B2': False,
  'B3': False,
  'Gain': 1.0,
  'Mono': False,
  'Solo': False,
  'Mute': False
}

blank = {f'in-{i}': blank_input for i in range(8)}

__ALL__ = ['connect']