import os
import posixpath
from pkg_resources import resource_filename
from subprocess import call
from script import app_name
from script.android import ADB_PATH



if __name__ == '__main__':
    app_dir = os.path.realpath(resource_filename(app_name, '.'))
    call([ADB_PATH, 'push', app_dir, posixpath.join(posixpath.sep, 'sdcard', 'kivy', app_name)])
