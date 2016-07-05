#!/usr/bin/env python3

'''
	Usage:
	afs -s /the/path/to/find 'pattern'
	afs /the/path/to/find 'pattern'
		1	/the/path/to/find/rsltfile1.cpp
		2	/the/path/to/find/rsltfile2.py
		3	/the/path/to/find/rsltfile3.rst


	afs -c subl -n ^2
		==> subl -n /the/path/to/find/rsltfile2

	afs -c rm ^3
		==> rm ^3

	sudo afs -c cp ^1 /usr/bin
		==> sudo cp /the/path/to/find/rsltfile1.cpp /usr/bin
'''

from pathlib import Path
import pickle as pk
import sys
import os
import argparse
from IPython.core.debugger import Tracer; set_trace = Tracer(colors='linux')

desc = \
'''
Andvanced file seeker:
	-seek out files meet a certain pattern
	-run command contain the file(s) seeked out before
	
'''

parser = argparse.ArgumentParser(description='Andvanced file seeker')
parser.add_argument('-p', '--pattern', nargs='?', help='pattern will be used to seek')
parser.add_argument('-d', '--direction', nargs='?', help='direction will be seeked')
parser.add_argument('-c', '--cmd', type=str, nargs='+', help='run command as followed this option flag. {^number} indecates the file number seeked out before')
parser.add_argument('-r', '--reproduct', action='store_true', help='reproduct the result seeked before')

args = parser.parse_args()

#process

in_windows = sys.platform.lower().startswith('win')
if in_windows:
	Path.abspath = property(fget=lambda self: Path.absolute(self).as_posix())
	placeholder = '#'
else:
	Path.abspath = property(fget=lambda self: Path.absolute(self).path)
	placeholder = '^'
tmpdir = in_windows and os.environ['temp'] or '/tmp'
logpath = Path(tmpdir) / '.asf.pypk'


def seek():
	if args.direction and args.pattern: #-p XXX -d XXX
		pathroot = Path(args.direction)
	elif args.direction: #only -d XXX
		print('Error: missing pattern. -d %s ignored'%args.direction)
		return
	elif args.pattern: #only -p XXX
		pathroot = Path('./')
	else:# -p & -d both none
		return

	starts_with_slash = args.pattern.startswith('/')
	pattern = starts_with_slash and args.pattern[1:] or args.pattern
	files = pathroot.glob(pattern)

	print('Search partter: %s from %s'%(pattern, pathroot.path))
	print('-'*16)

	rslt = []
	counter = 0

	def process(fn):
		nonlocal counter
		rslt.append(fn.abspath)
		print('\t\t', str(counter), fn)
		counter += 1

	def dump_log():		
		with open(logpath.path, 'wb') as f:
			pk.dump(rslt, f)

	def hint100_and_dump():
		if hint100_and_dump.__dict__!={}:
			return
		answer = input('Found more than 100 files, would you like to continue?\n[C/c/Y/y or about for any_other_key]')
		if answer not in ('y', 'Y', 'c', 'C'):
			print('Aborted by user!')
			dump_log()
			exit(0)
		hint100_and_dump.hinted = True

	fn = None
	while True:
		try:
			fn = next(files)
		except StopIteration:
			break
		except PermissionError as e:
			print(e)
			continue
		except KeyboardInterrupt as e:
			print(e)
			dump_log()
			exit(1)
		process(fn)
		if counter > 100:
			hint100_and_dump()
	dump_log()


##########################################################
def run_cmd():
	if args.cmd == None:
		exit(0)
	if type(args.cmd) == str:
		args.cmd = args.cmd.split(' ')
		print(args.cmd)
	try:
		with open(logpath.path, 'rb') as f:
			filelist = pk.load(f)
	except FileNotFoundError:
		print('No seek log, missing %s'%logpath.path)

	num = None
	command = ' '.join(args.cmd)
	#set_trace()
	for arg in args.cmd:
		if placeholder not in arg:
			continue
		try:
			num = int(arg.replace(placeholder, ''))
			set_trace()
			filename = filelist[num]
			filename = in_windows and filename or filename.replace(' ', '\x5c ')
			print(filename)
			command = command.replace(arg, filename)
		except ValueError:
			print('File number must be interger!')
			exit(-1)
	import subprocess
	subprocess.Popen(command)

def reproduct():
	if not args.reproduct:
		return
	counter = 0
	try:
		with open(logpath.path, 'rb') as f:
			filelist = pk.load(f)
	except FileNotFoundError:
		print('log file not found')
		exit(1)
	for fn in filelist:
		print('\t\t', str(counter), fn)
		counter += 1

if __name__ == '__main__':
	reproduct()
	seek()
	run_cmd()
