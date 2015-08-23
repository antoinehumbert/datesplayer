import os
import posixpath
from pkg_resources import resource_filename
from subprocess import call
from script import app_name



ADB_PATH = os.path.join('C:\\', 'Users', 'Antoine', 'AppData', 'Local', 'Android', 'android-sdk', 'platform-tools',
                        'adb.exe')

if __name__ == '__main__':
    app_dir = os.path.realpath(resource_filename(app_name, '.'))
    call([ADB_PATH, 'push', app_dir, posixpath.join(posixpath.sep, 'sdcard', 'kivy', app_name)])
