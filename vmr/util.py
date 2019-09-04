import os

PROJECT_DIR = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

def project_path(*parts):
  return os.path.join(PROJECT_DIR, *parts)

def merge_dicts(*srcs, dest={}):
  target = dest
  for src in srcs:
    for key, val in src.items():
      if isinstance(val, dict):
        node = target.setdefault(key, {})
        merge_dicts(val, dest=node)
      else:
        target[key] = val
  return target