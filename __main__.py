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