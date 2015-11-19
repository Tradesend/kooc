#!/usr/bin/python3

import sys, os, subprocess

def main(av):
    if not os.path.isfile(av):
        sys.exit('File not found : ' + av)
    koocinator(av)

def koocinator(path):
    cmd = ['python3', '__main__.py', path]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        sys.exit(err.decode('utf-8'))
    fname, ext = path.split('.')
    if ext == 'kc':
        fname += '.c'
    elif ext == 'kh':
        fname += '.h'
    txt = out.decode('utf-8')
    if '# include ' in txt:
        l = txt.split('\n')
        for li in l:
            if '# include ' in li:
                main(li.split('\"')[1].replace('.h', '.kh'))
    with open(fname, 'w') as infile:
        infile.write(txt)
    if ext == 'kc':
        os.system('gcc ' + fname + ' -o ' + fname.split('.')[0])

for av in sys.argv[1:]:
    main(av)
