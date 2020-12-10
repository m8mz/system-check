import psutil
import sys

def bytes2human(n):
	# http://code.activestate.com/recipes/578019
	# >>> bytes2human(10000)
	# '9.8K'
	# >>> bytes2human(100001221)
	# '95.4M'
	symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
	prefix = {}
	for i, s in enumerate(symbols):
		prefix[s] = 1 << (i + 1) * 10
	for s in reversed(symbols):
		if n >= prefix[s]:
			value = float(n) / prefix[s]
			return '%.1f%s' % (value, s)
	return "%sB" % n


def disk(path=None, warning=80, critical=90):
  """
  Returns the disk utilization for either all disks or specified.
  """
  if not path:
    disks = psutil.disk_partitions()
    mountpoints = [ m.mountpoint for m in disks ]
    status = "OK"
    passed_threshold = []
    for mount in mountpoints:
      stats = psutil.disk_usage(mount)
      if stats.percent > critical:
        if status != "CRITICAL":
          status = "CRITICAL"
        passed_threshold.append(f"{mount} {stats.percent}%")
      elif stats.percent > warning:
        if status != "CRITICAL" or status != "WARNING":
          status = "WARNING"
        passed_threshold.append(f"{mount} {stats.percent}%")
    if passed_threshold:
      data = f"Disk {status} - {', '.join(passed_threshold)}"
    else:
      data = f"Disks {status}"
  else:
    try:
      stats = psutil.disk_usage(path)
    except FileNotFoundError as e:
      print(e, file=sys.stderr)
      return 1
    else:
      status = "OK"
      exit_code = 0
      if stats.percent > critical:
        status = "CRITICAL"
        exit_code = 2
      elif stats.percent > warning:
        status = "WARNING"
        exit_code = 1
      data = f"Disk {path} {status} - {stats.percent}% | total={stats.total} used={stats.used} free={stats.free}"
  return {'exit_code': exit_code, 'status': data}


def io(perdisk=False):
  """
  Returns the disk IO statistics. No warning or critical setting, couldn't think of way to calculate this.
  """
  if perdisk:
    stats = psutil.disk_io_counters(perdisk=perdisk)
    stats_arr = []
    for disk, stat in stats.items():
      stats_arr.append(f"{disk}_read_bytes={stat.read_bytes}, {disk}_write_bytes={stat.write_bytes}")
    data = f"Disk IO OK | {', '.join(stats_arr)}"
  else:
    stats = psutil.disk_io_counters()
    data = f"Disk IO OK | read_bytes={stats.read_bytes} write_bytes={stats.read_bytes}"
  return {'exit_code': 0, 'status': data}
