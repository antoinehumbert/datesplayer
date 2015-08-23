from setuptools import setup, find_packages
from babel.messages import frontend as babel



setup(name='datesplayer',
      version='1.0',
      description='Dates Player Kivy Application',
      author='Antoine Humbert',
      author_email='antoine.humbert@gmail.com',
      url='',
      packages=find_packages(exclude=['datesplayer.tests.*']),
      install_requires = ['kivy==1.9.0', 'plyer'],

      cmdclass = {'compile_catalog': babel.compile_catalog,
                  'extract_messages': babel.extract_messages,
                  'init_catalog': babel.init_catalog,
                  'update_catalog': babel.update_catalog},
      message_extractors = {'datesplayer': [('**.py', 'python', None),
                                            ('**.kv', 'python', None)]},
      )