import os
import sys
from pkg_resources import resource_filename
from subprocess import call
from script import app_name



GARDENS = ['tickline', 'roulettescroll', 'roulette']



if __name__ == '__main__':
    garden_path = os.path.join(os.path.dirname(sys.executable), 'garden.bat')
    app_dir = os.path.realpath(resource_filename(app_name, '.'))
    cur_dir = os.getcwd()
    os.chdir(app_dir)
    try:
        for garden in GARDENS:
            call([garden_path, 'install', '--app', garden])
    finally:
        os.chdir(cur_dir)
