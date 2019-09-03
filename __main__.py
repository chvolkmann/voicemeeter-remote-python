import vmr
import time

def merge(target, *srcs):
  for src in srcs:
    for key, val in src.items():
      if isinstance(val, dict):
        node = target.setdefault(key, {})
        merge(node, val)
      else:
        target[key] = val
  return target

profiles = {
  '_default': {
    **{f'in-{i}': vmr.input_strip_config for i in range(8)}
  },
  'main': {
    'in-5': dict(A1=True)
  },
  'test': {
    **{f'in-{i}': dict(A4=True, A5=True) for i in range(8)}
  }
}

def profile(target):
  dict = profiles[target] if isinstance(target, str) else target
  return merge({}, profiles['_default'], dict)

with vmr.connect('potato') as remote:
  remote.apply(**profile('test'))
  time.sleep(1)
  remote.apply(**profile('_default'))