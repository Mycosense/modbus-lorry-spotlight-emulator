from setuptools import setup
import os

setup(name='mys_emulator',
      python_requires=">=3.10",
      description='',
      url='https://github.com/Mycosense/modbus-lorry-spotlight-emulator',
      author='Nicolas Uffer',
      author_email='nu@mycosense.ch',
      license='Copyright 2025 Mycosense SA',
      packages=['mys_emulator'],
      entry_points={
          'console_scripts': [
              'emulate_spotlight=mys_emulator.emulate_spotlight:main',
          ]
      },
      install_requires=[
          'pymodbus==3.8.6', 'pyserial==3.5',
      ],

      include_package_data=True,
      use_scm_version=True,
      setup_requires=['setuptools_scm==6.4.2'],
      zip_safe=False)
