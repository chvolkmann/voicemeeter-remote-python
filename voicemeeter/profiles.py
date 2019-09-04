import os
import toml
from . import kinds
from .errors import VMRError
from .util import project_path, merge_dicts

profiles = {}

def _make_blank_profile(kind):
  num_A, num_B = kind.layout
  input_strip_config = {
    'gain': 0.0,
    'solo': False,
    'mute': False,
    'mono': False,
    **{f'A{i}': False for i in range(1, num_A+1)},
    **{f'B{i}': False for i in range(1, num_B+1)}
  }
  output_strip_config = {
    'gain': 0.0,
    'mute': False
  }
  return {
    **{f'in-{i}': input_strip_config for i in range(num_A+num_B)},
    **{f'out-{i}': output_strip_config for i in range(num_A+num_B)}
  }

def _make_base_profile(kind):
  num_A, num_B = kind.layout
  blank = _make_blank_profile(kind)
  overrides = {
    **{f'in-{i}': dict(B1=True) for i in range(num_A)},
    **{f'in-{i}': dict(A1=True) for i in range(num_A, num_A+num_B)}
  }
  abc = merge_dicts(blank, overrides)
  return abc

for kind in kinds.all:
  profiles[kind.id] = {
    'blank': _make_blank_profile(kind),
    'base': _make_base_profile(kind)
  }

# Load profiles from config files in profiles/<kind_id>/<profile>.toml
if os.path.exists(project_path('profiles')):
  for kind in kinds.all:
    profile_folder = project_path('profiles', kind.id)
    if os.path.exists(profile_folder):
      filenames = [f for f in os.listdir(profile_folder) if f.endswith('.toml')]
      configs = {}
      for filename in filenames:
        name = filename[:-5] # strip of .toml extension
        try:
          configs[name] = toml.load(project_path('profiles', kind.id, filename))
        except toml.TomlDecodeError:
          print(f'Invalid TOML profile: {kind.id}/{filename}')
      
      for name, cfg in configs.items():
        print(f'Loaded profile {kind.id}/{name}')
        profiles[kind.id][name] = cfg