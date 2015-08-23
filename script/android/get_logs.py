import os
import posixpath
from pkg_resources import resource_filename
from subprocess import call
from script import app_name
from script.android import ADB_PATH



if __name__ == '__main__':
    logs_dir = os.path.realpath(resource_filename(app_name, '../../logs'))
    call([ADB_PATH, 'pull', posixpath.join(posixpath.sep, 'sdcard', 'kivy', app_name, '.kivy', 'logs'), logs_dir])
