import subprocess as sp
import time

from .remote import connect as remote
from .driver import vm_subpath
from . import kinds

def launch(kind_id, delay=1):
  """ Starts Voicemeeter. """
  kind = kinds.get(kind_id)
  sp.Popen([vm_subpath(kind.executable)])
  time.sleep(delay)

__ALL__ = ['launch', 'remote']