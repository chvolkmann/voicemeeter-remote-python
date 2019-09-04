import vmr
import time

profiles = {
  'default': {
    **{f'in-{i}': vmr.blank_input for i in range(8)}
  },
  'main': {
    **{f'in-{i}': dict(A1=True) for i in range(8)}
  },
  'vr': {
    **{f'in-{i}': dict(A4=True) for i in range(5,8)}
  },
  'vr-tv': {
    **{f'in-{i}': dict(A2=True, A4=True) for i in range(5,8)}
  }
}

def resolve(nameOrDict):
  return profiles[nameOrDict] if isinstance(nameOrDict, str) else nameOrDict

def merge(target, *srcs):
  for src in srcs:
    for key, val in src.items():
      if isinstance(val, dict):
        node = target.setdefault(key, {})
        merge(node, val)
      else:
        target[key] = val
  return target

def profile(target, base='default'):
  base = base or {}
  return merge({}, resolve(base), resolve(target))

profiles['blank'] = profile(vmr.blank, base=None)
profiles['default'] = profile({f'in-{i}': dict(A1=True) for i in range(5,8)})

vmr.open()
with vmr.connect('potato') as remote:
  remote.apply(profile('vr-tv', base='blank'))
  time.sleep(1)
  remote.apply(profile('default'))