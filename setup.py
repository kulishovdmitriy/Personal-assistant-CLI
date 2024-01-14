from setuptools import setup

setup(
   name='Personal-assistant-CLI',
   version='0.1',
   description='Personal assistant',
   url="https://github.com/Dimon4444eg/Personal-assistant-CLI",
   author='Dmitriy Kylishov',
   author_email='kylishovdimka@ukr.net',
   license='MIT',
   packages=['Personal-assistant-CLI'],
   install_requires=[],
   entry_points={
       'console_scripts': [
           'Personal-assistant-CLI = Personal-assistant-CLI.main: main'
       ]
   }
)
