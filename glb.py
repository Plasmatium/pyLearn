#!/usr/bin/env python3.5

from pathlib import Path
import pickle as pk
import sys
import os

argv = sys.argv
search_root = ''
argn = len(argv)

def main():
	if argv[1].startswith('^'):
		do_command()
		exit(0)

	if argn==3:
		search_root = argv[1]
		search_pattern = argv[2]
	elif argn==2:
		search_root = './'
		search_pattern = argv[1]
	else:
		print('Error number on args!')
		print(argv)
		exit(1)

	pathobj = Path(search_root)
	files = pathobj.glob(search_pattern)

	print('Search partter: %s from %s'%(search_pattern, search_root))
	print('-'*16)

	counter = 0
	for fn in files:
		counter += 1
		print('\t'+str(counter)+'\t\t',fn)

		if counter >= 100:
			break

	try:
		fn = next(files)
		counter += 1
	except StopIteration:
		if counter==0:
			print('Nothing found there!')
		exit(0)

	answer = input('Found more than 100 files, would you like to continue?\n[C/c/Y/y or about for any_other_key]')
	if answer not in ('y', 'Y', 'c', 'C'):
		print('Aborted by user!')
		exit(0)

	print('\t'+str(counter)+'\t\t',fn)
	for fn in files:
		counter += 1
		print('\t'+str(counter)+'\t\t',fn)
# glob ^subl^-n^2333 ==> subl -n file#2333
def do_command():
	#ToDo
	cmd = ' '.join(argv[1:])
	os.system()

if __name__ == '__main__':
	main()