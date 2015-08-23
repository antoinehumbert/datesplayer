import os
from pkg_resources import resource_filename
from subprocess import call
from script import app_name

if __name__ == '__main__':
    src_dir = os.path.realpath(resource_filename(app_name, '..'))
    setup = os.path.join(src_dir, 'setup.py')
    i18n_dir = os.path.join(src_dir, app_name, 'i18n')
    call(['python', setup, 'compile_catalog', '-d', i18n_dir, '--statistics'])
