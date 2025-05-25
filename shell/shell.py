import cfpl

while True:
  text = input('cfpl > ')
  result, error = cfpl.run('<stdin>', text)
  
  if error: print(error.as_string())
  else: print(result)