import psutil

def procs(warning=300, critical=500):
  """
  Return the number of processes running.
  """
  num_procs = len(psutil.pids())
  status = "OK"
  exit_code = 0
  if num_procs > critical:
    status = "CRITICAL"
    exit_code = 2
  elif num_procs > warning:
    status = "WARNING"
    exit_code = 1
  data = f"Processes {status} - {num_procs} | procs={num_procs}"
  return {'exit_code': exit_code, 'status': data}
