class VMRError(Exception):
  pass

class VMRDriverError(VMRError):
  def __init__(self, fn_name, retval):
    self.function = fn_name
    self.retval = retval

    super().__init__(f'VMR#{fn_name}() returned {retval}')