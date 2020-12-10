import psutil

def cpu_percent(warning=80, critical=90):
  """
  Returns the CPU percentage of user, nice, system together
  """
  percent = psutil.cpu_percent()
  status = "OK"
  exit_code = 0
  if percent > critical:
    status = "CRITICAL"
    exit_code = 2
  elif percent > warning:
    status = "WARNING"
    exit_code = 1
  data = f"CPU {status} - {percent}% | cpu={percent}%"
  return {"exit_code": exit_code, "status": data}


def cpu_times_percent(percpu=False, warning=80, critical=90):
  """
  Returns the CPU stats for each following val user, nice, system, and idle.
  This is an average for all CPU cores. Changing percpu to True will return for each cpu.
  """
  if not percpu:
    stats = psutil.cpu_times_percent()
    status = "OK"
    exit_code = 0
    if stats.user > critical or stats.nice > critical or stats.system > critical:
      status = "CRITICAL"
      exit_code = 2
    elif stats.user > warning or stats.nice > warning or stats.system > warning:
      status = "WARNING"
      exit_code = 1
    data = f"CPU Stats {status} - User={stats.user}%, Nice={stats.nice}%, System={stats.system}% | user={stats.user}%, nice={stats.nice}%, system={stats.system}%, idle={stats.idle}%"
    return {'exit_code': exit_code, 'status': data}


def cpu_freq():
  """
  Returns the CPU frequency with warning and critical set to the min and max of whats set by the CPU.
  """
  freq = psutil.cpu_freq()
  status = "OK"
  exit_code = 0
  if freq.current > freq.max or freq.current < freq.min:
    status = "CRITICAL"
    exit_code = 2
  data = f"CPU Frequency {status} - {freq.current} | current={freq.current}, min={freq.min}, max={freq.max}"
  return {'exit_code': exit_code, 'status': data}


def load_average(w1=None, w2=None, w3=None, c1=None, c2=None, c3=None):
  """
  Returns the CPU load average. The input for this function follows the following structure.
  w1 = Warning threshold for 1 minute
  w2 = Warning threshold for 5 minutes
  w3 = Warning threshold for 15 minutes
  c1 = Critical threshold for 1 minute
  c2 = Critical threshold for 5 minutes
  c3 = Critical threshold for 15 minutes
  """
  number_of_cores = psutil.cpu_count(logical=False)
  # if w1-3 and/or c1-3 are None, calculate the settings based on number of physical cores
  if not w1:
    w1 = number_of_cores * 1
  if not w2:
    w2 = number_of_cores * 0.9
  if not w3:
    w3 = number_of_cores * 0.8
  if not c1:
    c1 = number_of_cores * 1.5
  if not c2:
    c2 = number_of_cores * 1.3
  if not c3:
    c3 = number_of_cores * 1.1
  load_avg = psutil.getloadavg()
  status = "OK"
  exit_code = 0
  if load_avg[0] > c1 or load_avg[1] > c2 or load_avg[2] > c3:
    status = "CRITICAL"
    exit_code = 2
  elif load_avg[0] > w1 or load_avg[1] > w2 or load_avg[2] > w3:
    status = "WARNING"
    exit_code = 1
  data = f"Load Avg {status} - {load_avg[0]},{load_avg[1]},{load_avg[2]} | 1min={load_avg[0]}, 5min={load_avg[1]}, 15min={load_avg[2]}"
  return {'exit_code': exit_code, 'status': data}
