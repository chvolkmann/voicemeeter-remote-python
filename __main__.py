from vmr import VMRemote
import time

with VMRemote.make('potato') as remote:
  for _ in range(5):
    print(remote.inputs[0].mono)