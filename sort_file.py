# coding: utf-8

import sys
import os
import shutil
import glob

config = 'config.txt'
rules = []

replaces = {
}

def errorExit(message, code = -1):
	print(message)
	sys.exit(code)

# Check arguments
if len(sys.argv) != 2:
	errorExit('Usage: {[0]} TARGET_DIR'.format(sys.argv))

target = sys.argv[1]

# Check rules
with open(config, encoding = 'utf-8') as f:
	for l in f.readlines():
		l = l.split('\t')
		rules.append({
			'key': l[0].strip(),
			'dest': l[1].strip()
		})
if len(rules) < 1:
	errorExit('No rules defined.')

# Check target path
if not os.path.exists(target) or not os.path.isdir(target):
	errorExit('The directory you specified is not a directory.')

# Scan target dir
for file in os.listdir(target):
	path = os.path.join(target, file)

	# Currently, recursive scanning is disabled
	if os.path.isdir(path):
		print('{} is a directory. Skipping.'.format(path))
		continue
	
	# Check all rules
	for i in rules:
		key = i['key']
		dest = i['dest']
		if key in file:
			sys.stdout.write('Copying {} ... '.format(file))

			# Check whether destination file exists
			if os.path.exists(os.path.join(dest, file)):
				print('already exists. Renaming...')
				name, ext = os.path.splitext(file)
				count = len(glob.glob(os.path.join(dest, "*" + ext)))
				dest = os.path.join(dest, name + " #{:02d}".format(count) + ext)
			
			# replace characters in filename
			for k, v in replaces.items():
				dest = dest.replace(k, v)
			print(dest)
			
			# Do move
			try:
				shutil.move(path, dest)
			except:
				print('failed. Skipping...')
			else:
				print('done.')
			break
			
	else:
		print("'{}' doesn't match any rules. Skipping.".format(file))
