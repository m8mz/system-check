import psutil

def net_connections(port=[], warning=10, critical=20):
  """
  Return the network connections that are established. If provided a port will return connections for that.
  """
  if port:
    conns = psutil.net_connections()
    remote_conns = [ c for c in conns if c.raddr and c.status == "ESTABLISHED" and c.laddr.port in port ]
    num_conns = len(remote_conns)
    status = "OK"
    exit_code = 0
    if num_conns > critical:
      status = "CRITICAL"
      exit_code = 2
    elif num_conns > warning:
      status = "WARNING"
      exit_code = 1
    data = f"Network Connections {port} {status} - {num_conns} | {port}_connections={num_conns}"
  else:
    conns = psutil.net_connections()
    remote_conns = [ c for c in conns if c.raddr and c.status == "ESTABLISHED" ]
    num_conns = len(remote_conns)
    status = "OK"
    exit_code = 0
    if num_conns > critical:
      status = "CRITICAL"
      exit_code = 2
    elif num_conns > warning:
      status = "WARNING"
      exit_code = 1
    data = f"Network Connections {status} - {num_conns} | connections={num_conns}"
  return {'exit_code': exit_code, 'status': data}
