# Voicemeeter Remote
A Python API to [Voicemeeter](https://www.vb-audio.com/Voicemeeter/potato.htm), a virtual audio mixer for Windows.

This work-in-progress package wraps the [Voicemeeter Remote C API](https://forum.vb-audio.com/viewtopic.php?f=8&t=346) and provides a higher-level interface for developers.

Tested against Voicemeeter Potato, release from September 2019.


## Prerequisites
- Voicemeeter 1 (Basic), 2 (Banana) or 3 (Potato)
- Python 3.6+

## Installation
```
git clone https://github.com/Freemanium/voicemeeter-remote-python
cd voicemeeter-remote-python
pip install .
```

## Usage
```python
import voicemeeter

# Can be 'basic', 'banana' or 'potato'
kind = 'potato'

# Ensure that Voicemeeter is launched
voicemeeter.launch(kind)

with voicemeeter.remote(kind) as vmr:
  # Set the mapping of the second input strip
  vmr.inputs[1].A4 = True
  print(f'Output A4 of Strip {vmr.inputs[1].label}: {vmr.inputs[1].A4}')

  # Set the gain slider of the leftmost output bus
  vmr.outputs[0].gain = -6.0

  # Also supports assignment through a dict
  vmr.apply({
    'in-5': dict(A1=True, B1=True, gain=-6.0),
    'out-2': dict(mute=True)
  })

  # Resets all UI elements to a base profile
  vmr.reset()
```
Or if you want to use the API outside of a with statment
```python
import voicemeeter

# Can be 'basic', 'banana' or 'potato'
kind = 'potato'

# Ensure that Voicemeeter is launched
voicemeeter.launch(kind)

vmr = voicemeeter.remote(kind)
vmr.login()
# Set the mapping of the second input strip
vmr.inputs[1].A4 = True
print(f'Output A4 of Strip {vmr.inputs[1].label}: {vmr.inputs[1].A4}')

# Set the gain slider of the leftmost output bus
vmr.outputs[0].gain = -6.0

# Also supports assignment through a dict
vmr.apply({
'in-5': dict(A1=True, B1=True, gain=-6.0),
'out-2': dict(mute=True)
})

# Resets all UI elements to a base profile
vmr.reset()
vmr.logout()
```

## Profiles
Profiles through config files are supported.
```
mkdir profiles
mkdir profiles/potato
touch profiles/potato/mySetup.toml
```

A config can contain any key that `remote.apply()` would accept. Additionally, `extends` can be provided to inherit from another profile. Two profiles are available by default:
- `blank`, all inputs off and all sliders to `0.0`
- `base`, all physical inputs to `A1`, all virtual inputs to `B1`, all sliders to `0.0`

Sample `mySetup.toml`
```toml
extends = 'base'
[in-0]
mute = 1

[in-5]
A1 = 0
A2 = 1
A4 = 1
gain = 0.0

[in-6]
A1 = 0
A2 = 1
A4 = 1
gain = 0.0
```

## API
### Kinds
A *kind* specifies a major Voicemeeter version. Currently this encompasses
- `basic`: [Voicemeeter](https://www.vb-audio.com/Voicemeeter/index.htm)
- `banana`: [Voicemeeter Banana](https://www.vb-audio.com/Voicemeeter/banana.htm)
- `potato`: [Voicemeeter Potato](https://www.vb-audio.com/Voicemeeter/potato.htm)

#### `voicemeeter.launch(kind_id, delay=1)`
Launches Voicemeeter. If Voicemeeter is already launched, it is brought to the front. Wait for `delay` seconds after a launch is dispatched.

#### `voicemeeter.remote(kind_id, delay=0.015)`
Factory function for remotes. `delay` specifies a cooldown time after every command in seconds. Returns a `VMRemote` based on the `kind_id`.  
Use it with a context manager
```python
with voicemeeter.remote('potato') as vmr:
  vmr.inputs[0].mute = True
```

### `VMRemote` (higher level)
#### `vmr.type`
The kind of the Voicemeeter instance.

#### `vmr.version`
A tuple of the form `(v1, v2, v3, v4)`.

#### `vmr.inputs`
An `InputStrip` tuple, containing both physical and virtual.
#### `vmr.outputs`
An `OutputBus` tuple, containing both physical and virtual.

#### `vmr.show()`
Shows Voicemeeter if it's minimized. No effect otherwise.
#### `vmr.shutdown()`
Closes Voicemeeter.
#### `vmr.restart()`
Restarts Voicemeeter's audio engine.

#### `vmr.apply(mapping)`
Updates values through a dict.  
Example:
```python
vmr.apply({
    'in-5': dict(A1=True, B1=True, gain=-6.0),
    'out-2': dict(mute=True)
  })
```
#### `vmr.apply_profile(profile_name)`
Loads a profile.
#### `vmr.reset()`
Resets everything to the `base` profile.

### `InputStrip`
Any property is gettable and settable.
- `label`: string
- `solo`: boolean
- `mute`: boolean
- `gain`: float, from -60.0 to 12.0
- `eqgain1`: float, from -12.0 to 12.0
- `eqgain2`: float, from -12.0 to 12.0
- `eqgain3`: float, from -12.0 to 12.0
- `comp`: float, from 0.0 to 10.0
- `gate`: float, from 0.0 to 10.0
- Output mapping (e.g. `A1`, `B3`, etc.): boolean, depends on the Voicemeeter kind
- `apply()`: Works similar to `vmr.apply()`
### `OutputBus`
Any property is gettable and settable.
- `mute`: boolean
- `gain`: float, from -60.0 to 12.0
- `apply()`: Works similar to `vmr.apply()`

### `VMRemote` (lower level)
#### `vmr.dirty`
`True` iff UI parameters have been updated. Use this if to poll for UI updates.

#### `vmr.get(param_name, string=False)`
Calls the C API's parameter getters, `GetParameterFloat` or `GetParameterStringW` respectively. Tries to cache the value on the first call and updates the cached value if `vmr.dirty` is `True`.

#### `vmr.set(param_name, value)`
Calls the C API's parameter getters, `SetParameterFloat` or `SetParameterStringW` respectively.

### Errors
- `errors.VMRError`: Base Voicemeeter Remote error class.
- `errors.VMRDriverError`: Raised when a C API function returns an unexpected value.

## Resources
- [Voicemeeter Remote C API](https://forum.vb-audio.com/viewtopic.php?f=8&t=346)
