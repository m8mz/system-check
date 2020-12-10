#!/usr/bin/env python3

import psutil
import argparse
import sys
import check_cpu
import check_disk
import check_mem
import check_net
import check_procs
import check_users

parser = argparse.ArgumentParser(prog='System Check')
subparsers = parser.add_subparsers(dest='command',help='sub-command help')

# cpu check sub parser
parser_cpu = subparsers.add_parser('cpu', help='cpu performance')
parser_cpu.add_argument('--percent', default=False, action='store_true', help='percentage')
parser_cpu.add_argument('--stats', default=False, action='store_true', help='cpu stats')
parser_cpu.add_argument('--timespercent', default=False, action='store_true', help='cpu times percent')
parser_cpu.add_argument('--freq', default=False, action='store_true', help='cpu frequency')
parser_cpu.add_argument('--load', default=False, action='store_true', help='cpu load')

# memory check sub parser
parser_memory = subparsers.add_parser('memory', help='memory performance')
parser_memory.add_argument('--virtual', default=False, action='store_true', help='memory')
parser_memory.add_argument('--swap', default=False, action='store_true', help='swap')

# disk check sub parser
parser_disk = subparsers.add_parser('disk', help='disk performance')
parser_disk.add_argument('--all', default=False, action='store_true', help='disk usage check for all disks')
parser_disk.add_argument('--usage', help='disk usage')
parser_disk.add_argument('--ioall', default=False, action='store_true', help='disk io counters')
parser_disk.add_argument('--ioper', default=False, action='store_true', help='disk io counters')

# network check sub parser
parser_network = subparsers.add_parser('net', help='network performance')
parser_network.add_argument('--conn', help='network connections')

# process check sub parser
parser_process = subparsers.add_parser('process', help='process management')
parser_process.add_argument('--count', default=False, action='store_true', help='count number of procs')



if __name__ == "__main__":
  args = parser.parse_args()
  if not args.command:
    sys.exit("must provide a command")

  if args.command == "cpu":
    if args.percent:
      result = check_cpu.cpu_percent()
      print(result)
    elif args.stats:
      result = check_cpu.cpu_times_percent()
      print(result)
    elif args.freq:
      result = check_cpu.cpu_freq()
      print(result)
    elif args.load:
      result = check_cpu.load_average()
      print(result)
    else:
      sys.exit("must provide a flag")
  elif args.command == "memory":
    if args.virtual:
      result = check_mem.memory()
      print(result)
    elif args.swap:
      result = check_mem.swap()
      print(result)
    else:
      sys.exit("must provide a flag")
  elif args.command == "disk":
    if args.all:
      result = check_disk.disk()
      print(result)
    elif args.usage:
      result = check_disk.disk(args.usage)
      print(result)
    elif args.ioall:
      result = check_disk.io()
      print(result)
    elif args.ioper:
      result = check_disk.io(perdisk=True)
      print(result)
    else:
      sys.exit("must provide a flag")
