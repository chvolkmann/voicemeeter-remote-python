import vmr
import time

vmr.open('potato')
with vmr.connect('potato') as remote:
  remote.apply_profile('fvr')