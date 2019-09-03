from collections import namedtuple
from .errors import VMRError

VMKind = namedtuple('VMKind', ['id', 'name', 'layout'])

_kind_map = {
  'basic': VMKind('basic', 'Basic', (2,1)),
  'banana': VMKind('banana', 'Banana', (3,2)),
  'potato': VMKind('potato', 'Potato', (5,3))
}

def get(kind_id):
  try:
    return all[kind_id]
  except KeyError:
    raise VMRError(f'Invalid Voicemeeter kind: {kind_id}')

all = list(_kind_map.values())