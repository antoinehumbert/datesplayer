import os
import glob

SDK_PATH = os.path.join(os.path.expandvars('${LOCALAPPDATA}'), 'Android', 'android-sdk')
ADB_PATH = os.path.join(SDK_PATH, 'platform-tools', 'adb.exe')
ZIPALIGN_PATH = os.path.join(glob.glob(os.path.join(SDK_PATH, 'build-tools', '*'))[0], 'zipalign')
