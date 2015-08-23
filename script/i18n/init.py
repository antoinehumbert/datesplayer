import os
from pkg_resources import resource_filename
from subprocess import call
from script import app_name

LANGUAGES = ['fr']

if __name__ == '__main__':
    src_dir = os.path.realpath(resource_filename(app_name, '..'))
    setup = os.path.join(src_dir, 'setup.py')
    i18n_dir = os.path.join(src_dir, app_name, 'i18n')
    for lang in LANGUAGES:
        call(['python', setup, 'init_catalog', '-l', lang, '-i', os.path.join(i18n_dir, '{}.pot'.format(app_name)),
              '-d', i18n_dir])
