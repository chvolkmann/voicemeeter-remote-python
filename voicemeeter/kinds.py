from collections import namedtuple
from .errors import VMRError

"""
Represents a major version of Voicemeeter and describes
its strip layout.
"""
VMKind = namedtuple('VMKind', ['id', 'name', 'layout', 'executable'])

_kind_map = {
  'basic': VMKind('basic', 'Basic', (2,1), 'voicemeeter.exe'),
  'banana': VMKind('banana', 'Banana', (3,2), 'voicemeeterpro.exe'),
  'potato': VMKind('potato', 'Potato', (5,3), 'voicemeeter8.exe')
}

def get(kind_id):
  try:
    return _kind_map[kind_id]
  except KeyError:
    raise VMRError(f'Invalid Voicemeeter kind: {kind_id}')

all = list(_kind_map.values())