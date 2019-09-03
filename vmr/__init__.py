from .remote import VMBasicRemote, VMBananaRemote, VMPotatoRemote
from .errors import VMRError

def connect(version, *args, **kwargs):
  if version in (1, 'basic'):
    return VMBasicRemote(*args, **kwargs)
  elif version in (2, 'banana'):
    return VMBananaRemote(*args, **kwargs)
  elif version in (3, 'potato'):
    return VMPotatoRemote(*args, **kwargs)
  else:
    raise VMRError(f'Invalid Voicemeeter version: {version}')

__ALL__ = ['connect']