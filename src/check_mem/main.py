import psutil

def memory(warning=80, critical=90):
  """
  Returns the memory utlization statistics.
  """
  mem = psutil.virtual_memory()
  status = "OK"
  exit_code = 0
  if mem.percent > critical:
    status = "CRITICAL"
    exit_code = 2
  elif mem.percent > warning:
    status = "WARNING"
    exit_code = 1
  data = f"Memory {status} - {mem.percent}% | total={mem.total}, available={mem.available}, used={mem.used}, free={mem.free}"
  return {'exit_code': exit_code, 'status': data}


def swap(warning=50, critical=70):
  """
  Returns the swap utilization statistics.
  """
  swap = psutil.swap_memory()
  status = "OK"
  exit_code = 0
  if swap.percent > critical:
    status = "CRITICAL"
    exit_code = 2
  elif swap.percent > warning:
    status = "WARNING"
    exit_code = 1
  data = f"Swap {status} - {swap.percent}% | total={swap.total}, used={swap.used}, free={swap.free}"
  return {'exit_code': exit_code, 'status': data}
