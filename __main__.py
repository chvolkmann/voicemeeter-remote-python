from vmr import VMRemote
import time

with VMRemote.make('potato') as remote:
  print(remote.inputs[0].device_name)