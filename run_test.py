#!/bin/python3

import sys, os, subprocess

if not os.path.isfile(sys.argv[1]):
    sys.exit('File not found : ' + sys.argv[1])

cmd = ['python', '__main__.py', sys.argv[1]]
p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
out, err = p.communicate()

fname, ext = sys.argv[1].split('.')
# fname = fname.split('/')[1:][0]
if ext == 'kc':
    fname += '.c'
elif ext == 'kh':
    fname += '.h'
with open(fname, 'w') as infile:
    infile.write(out.decode('utf-8'))
if ext == 'kc':
    try:
        os.system('gcc ' + fname + ' -o ' + fname.split('.')[0])
    except:
        print('Can\'not compile.')
