#!/usr/bin/env python

import os
import glob
import sys
from subprocess import call

app_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
SOURCE_DIR = glob.glob(os.path.join(os.path.sep, 'media', 'sf_*', '*', app_name, 'src', app_name))[0]
DEPLOY_DIR = os.path.join(os.path.expanduser('~'), 'deploy', app_name)



if __name__ == '__main__':
    if not os.path.exists(DEPLOY_DIR):
        os.makedirs(DEPLOY_DIR)
    call(['rsync', '-rt', '--delete', '--exclude', '/.buildozer', os.path.join(SOURCE_DIR, ''), DEPLOY_DIR])
    cur_dir = os.getcwd()
    os.chdir(DEPLOY_DIR)
    try:
        options = []
        args = []
        sys.argv.pop(0)
        while sys.argv:
            arg = sys.argv.pop(0)
            if arg.startswith('--'):
                options.append(arg)
            elif arg.startswith('-'):
                options.append(arg)
                arg = sys.argv.pop(0)
                options.append(arg)
            else:
                args.append(arg)
                break
        args.extend(sys.argv)
        call(['buildozer'] + options + ['android'] + args)
    finally:
        os.chdir(cur_dir)
