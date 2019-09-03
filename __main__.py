from vmr import VMRemote
import time

with VMRemote.make('potato') as remote:
  remote.outputs[2].mute = 0