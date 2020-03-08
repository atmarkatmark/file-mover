# coding: utf-8

import sys
import os
import shutil
import glob

config = 'config.txt'
rules = []
'''
rules = [
	{ 'key': '.txt', 'dest': '.\TEXT' },
	{ 'key': '.csv', 'dest': '.\CSV' }
]
'''

replaces = {
	'🈡': '　',
	'🈟': '　',
	'🈞': '　',
}

# sys.exit() with priting message to stdout
def errorExit(message, code = -1):
	print(message)
	sys.exit(code)

# Check arguments
if len(sys.argv) != 2:
	errorExit('Usage: {[0]} SOURCE_DIR'.format(sys.argv))

src = sys.argv[1]

# Check rules
with open(config, encoding = 'utf-8') as f:
	for l in f.readlines():
		l = l.split('\t')
		key = l[0].strip()
		dest = l[1].strip()

		# If dest is not a directory and the name is not used, then make the dir 
		if not os.path.isdir(dest):
			if not os.path.exists(dest):
				print("Destination '{}' doest not exist. Making...".format(dest))
				os.makedirs(dest)
			else:
				print("Destination '{}' is a file. Skipping.")
				continue
		
		# Append a rule to the list
		rules.append({
			'key': key,
			'dest': dest
		})
if len(rules) < 1:
	errorExit('No rules defined. Exiting...')

# Check source path
if not os.path.exists(src) or not os.path.isdir(src):
	errorExit('The directory you specified is not a directory.')

# Scan source dir
for filename in os.listdir(src):
	target = os.path.join(src, filename)

	# Currently, recursive scanning is disabled
	if os.path.isdir(target):
		print('{} is a directory. Skipping...'.format(target))
		continue
	
	# Check all rules
	for i in rules:
		key = i['key']
		dest = i['dest']
		if key in filename:
			sys.stdout.write('Copying {} ..... '.format(filename))
			sys.stdout.flush()

			# Check whether destination filename exists
			if os.path.exists(os.path.join(dest, filename)):
				print('already exists. Renaming...')
				name, ext = os.path.splitext(filename)
				count = len(glob.glob(os.path.join(dest, "*" + ext))) + 1
				dest = os.path.join(dest, name + " #{:02d}".format(count) + ext)
			else:
				dest = os.path.join(dest, filename)
			
			# Replace characters in filename
			for k, v in replaces.items():
				dest = dest.replace(k, v)
			
			# Do move
			try:
				shutil.move(target, dest)
			except:
				print('failed. Skipping...')
			else:
				print('done.')
			break
			
	else:
		print("'{}' doesn't match any rules. Skipping.".format(filename))
