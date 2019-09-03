import vmr

with vmr.connect('potato') as remote:
  remote.outputs[2].mute = 0