import os
import shutil
import glob
from subprocess import check_call
from script import app_name
from script.android import ZIPALIGN_PATH


KEYSTORE = 'android-release.keystore'
KEY_ALIAS = 'android-release'


if __name__ == '__main__':
    keystore_path = os.path.join(os.path.expandvars('${USERPROFILE}'), KEYSTORE)
    jarsigner = os.path.join(os.path.expandvars('${JAVA_HOME}'), 'bin', 'jarsigner')
    project_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    unsigned_apk_path = glob.glob(os.path.join(project_path, 'bin', '{}-*-release-unsigned.apk'.format(app_name)))[0]
    signed_apk_path = os.path.join(os.path.dirname(unsigned_apk_path),
                                   os.path.basename(unsigned_apk_path).replace('-unsigned', '-signed'))
    final_apk_path = os.path.join(os.path.dirname(unsigned_apk_path),
                                  os.path.basename(unsigned_apk_path).replace('-unsigned', ''))
    shutil.copy(unsigned_apk_path, signed_apk_path)
    try:
        check_call([jarsigner, '-verbose', '-sigalg', 'SHA1withRSA', '-digestalg', 'SHA1', '-keystore', keystore_path,
                    signed_apk_path, KEY_ALIAS])
        check_call([jarsigner, '-verify', '-verbose', '-certs', signed_apk_path])
        if os.path.exists(final_apk_path):
            os.unlink(final_apk_path)
        check_call([ZIPALIGN_PATH, '-v', '4', signed_apk_path, final_apk_path])
    finally:
        os.unlink(signed_apk_path)
