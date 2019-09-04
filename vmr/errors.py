class VMRError(Exception):
  """ Base error class for Voicemeeter Remote. """
  pass

class VMRDriverError(VMRError):
  """ Raised when a low-level C API function returns an unexpected value. """
  def __init__(self, fn_name, retval):
    self.function = fn_name
    self.retval = retval

    super().__init__(f'VMR#{fn_name}() returned {retval}')