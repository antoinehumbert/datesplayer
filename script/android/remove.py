import os
import posixpath
from pkg_resources import resource_filename
from subprocess import call
from script import app_name
from script.android import ADB_PATH



if __name__ == '__main__':
    call([ADB_PATH, 'shell', 'rm -rf "{}"'.format(posixpath.join(posixpath.sep, 'sdcard', 'kivy', app_name))])
