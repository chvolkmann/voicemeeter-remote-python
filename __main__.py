import vmr
import time

with vmr.connect('potato') as remote:
  remote.inputs[6].A4 = True
  time.sleep(1)
  remote.inputs[6].A4 = False
  print(remote.inputs[6].A4)