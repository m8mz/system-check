import psutil

def users(warning=5, critical=10):
  """
  Return the number of users logged in
  """
  users = len(psutil.users())
  status = "OK"
  exit_code = 0
  if users > critical:
    status = "CRITICAL"
    exit_code = 2
  elif users > warning:
    status = "WARNING"
    exit_code = 1
  data = f"Users {status} - {users} | users={users}"
  return {'exit_code': exit_code, 'status': data}
