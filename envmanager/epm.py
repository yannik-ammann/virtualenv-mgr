#!/usr/bin/env python

# CLI #
#######

from envmanager.envmanager import EnvManager
from envmanager.piphisto import PipHisto
import argparse
import os
import subprocess
import sys
from os import environ
from os import linesep

parser = argparse.ArgumentParser()

# parser.add_argument("filename", 
#                      help="file with paths to envs")

## ENVIRONMENT
parser.add_argument('environment', nargs='?', type=str,
                    help='path to file with paths to envs')
parser.add_argument('--envfreeze', action='store_true',
                    help='prints all the envs on .')
parser.add_argument('--searchpath', type=str,
                    help='path for envfreeze, where to search')

## ENVMANAGER
parser.add_argument('-f', '--find', type=str,
                    help='find app, use commas to search for more then one')
parser.add_argument("-l", "--freezelist", action='store_true',
                    help="pints the freeze_ist of all envs")
parser.add_argument("-i", "--install", type = str, 
                    help="installes an app, use commas to add more then one")
## PIP HISTO
parser.add_argument('-p', '--piphisto', action='store_true',
                    help='pip histogram')
parser.add_argument('-g', '--egg', action='store_true',
                    help='pip histogram takes eggs into consideration')
parser.add_argument('-v', '--version', action='store_true',
                    help='pip histogram takes versions into consideration')


args = ()
args = parser.parse_args()

cm_input = sys.stdin

#BASH_COMMAND = 'find /Users/yannik/ztemp -wholename "*/bin/activate" -prune | sed -e "s,/bin/activate,,g" | sed -e "s,//,/,g"'


if args.envfreeze:
    path = environ['PWD']
    if args.searchpath:
        path = args.searchpath
    find_popen = subprocess.Popen(['find', path, '-wholename', '*/bin/activate', '-prune'], stdout=subprocess.PIPE)
    subprocess.call(('sed', '-e', 's,/bin/activate,,g', '-e', 's,//,/,g'), stdin=find_popen.stdout)
    find_popen.wait()
    quit()


# if args.envfreeze:
#     path = environ['PWD']
#     if args.searchpath:
#         path = args.searchpath
#     subprocess.call(['find', args.searchpath, '-wholename', '*/bin/activate', '-prune', '|', 'sed', '-e', 's,/bin/activate,,g'],shell)
#     #subprocess.call(BASH_COMMAND.split())
#     #print '------'
#     #quit()
#     #print '------!'








if args.environment:
    env_list = file_name = None
    # python p.py -p "`python p.py --envfreeze`"
    if '\n' in args.environment:
        env_list = [n.replace('/bin/activate','') for n in args.environment.split(linesep)]
    else:
        file_name = args.environment
    em = EnvManager(file_name=file_name,env_list=env_list)
elif not sys.stdin.isatty():
    env_list = []
    for n in sys.stdin:
        env_list.append(n.replace(linesep,''))
    em = EnvManager(env_list=env_list)
else:
    if os.environ.get('VIRTUAL_ENV'):
        em = EnvManager(env_list=[os.environ['VIRTUAL_ENV']])
    else:
        print 'no active virtualenv and no --environment input, no pipe input'
        quit()





## ENVMANAGER CLI ##
####################

if args.find:
    find = []
    arg_input =  args.find
    if ',' in arg_input:
        find += arg_input.split(',')
    else:
        find = arg_input

if args.install:
    install = []
    arg_input =  args.install
    if ',' in arg_input:
        install += arg_input.split(',')
    else:
        install = arg_input



if args.install and args.find:
    em.up(find, install)
elif args.install:
    em.install(install)
elif args.find:
    em.finder(find)

if args.freezelist:
    for n in em.freezeList():
        print n




## PIPHISTO CLI ##
################## 

if args.piphisto:
    version = False
    egg = False
    if args.version:
        version = True
    if args.egg:
        egg = True
    ph = PipHisto(em.freezeList())
    ph.print_pip_histo(version=version,egg=egg)

