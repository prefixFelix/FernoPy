#!/usr/bin/env python3

from mpremote import main
import sys
import os
import subprocess
import platform


def call_cmd(args, src_path):
    if platform.system() == 'Windows':
        subprocess.call(args.insert(0, 'py -m'), cwd=src_path)
    elif platform.system() == 'Linux':
        subprocess.call(args, cwd=src_path)
    else:
        sys.exit('Platform not supported!')


def run_cmd(args):
    if platform.system() == 'Windows':
        subprocess.run(args.insert(0, 'py -m'))
    elif platform.system() == 'Linux':
        subprocess.run(args)
    else:
        sys.exit('Platform not supported!')


if __name__ == '__main__':
    print('+-------------- Install RX sniffing script --------------+')
    match len(sys.argv):
        case 1:
            port = input('Please enter the port: ')
        case 2:
            port = sys.argv[1]
        case _:
            sys.exit('Too many arguments!')
    print(f'[>] Connecting via {port}...\n'
          f'[>] Remove existing files...')

    # Remove all existing files
    # Credit: Romilly Cocking (https://gist.github.com/romilly/5a1ff86d1e4d87e084b76d5651f23a40)
    run_cmd(['mpremote', 'connect', port, 'exec', """
def _delete_all(dir='.'):
    for fi in os.ilistdir(dir):
        fn, ft = fi[0:2] # can be 3 or 4 items returned!
        fp = '%s/%s' % (dir, fn)
        print(f'removing {fp}') 
        if ft == 0x8000:
            os.remove(fp)
        else:
            _delete_all(fp)
            os.rmdir(fp)
_delete_all()
    """])

    # Copy new files
    print(f'[>] Copy new files...')
    src_path = os.path.abspath('src/rx/')
    call_cmd(['mpremote', 'connect', port, 'cp', '-r', '.', ':'], src_path)

    print('+-------------- Execute RX script on the µC --------------+')
    run_cmd(['mpremote', 'connect', port, 'reset'])
    run_cmd(['mpremote', 'connect', port, 'repl'])
