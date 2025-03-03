class FunctionValueError(Exception):
  """
  Exception raised for errors in the input values of the function.
  """
  def __init__(self, message):
    super().__init__(message)