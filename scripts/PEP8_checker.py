# run this script to see PEP8 errors
import os
import subprocess

if os.name == 'nt':
    subprocess.call(['flake.bat'])
else:
    subprocess.call(['./flake.sh'])
