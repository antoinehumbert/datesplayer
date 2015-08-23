import os
from pkg_resources import resource_filename
from subprocess import call
from script import app_name

if __name__ == '__main__':
    src_dir = os.path.realpath(resource_filename(app_name, '..'))
    setup = os.path.join(src_dir, 'setup.py')
    i18n_dir = os.path.join(src_dir, app_name, 'i18n')
    cur_dir = os.getcwd()
    os.chdir(src_dir)
    try:
        call(['python', setup, 'extract_messages', '-o', os.path.join(i18n_dir, '{}.pot'.format(app_name))])
    finally:
        os.chdir(cur_dir)
