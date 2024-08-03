def string_to_decimal(string):
  """Converts a string to a decimal integer.

  Args:
    string: The input string.

  Returns:
    The decimal representation of the string.
  """

  return int.from_bytes(string.encode('utf-8'), byteorder='big')

def decimal_to_string(decimal):
  """Converts a decimal integer to a string.

  Args:
    decimal: The decimal integer.

  Returns:
    The string representation of the decimal.
  """

  return decimal.to_bytes((decimal.bit_length() + 7) // 8, byteorder='big').decode('utf-8')

S = "SECRET STRING"

x = string_to_decimal(S)
y = decimal_to_string(x)
print(x,y)

print(decimal_to_string(6597373340904465883277793250887))