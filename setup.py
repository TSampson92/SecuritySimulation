# https://python-packaging.readthedocs.io/en/latest/minimal.html
from setuptools import setup

setup(name='security_simulation',
      version='0.1',
      description='The funniest joke in the world',
      url='https://github.com/TSampson92/SecuritySimulation',
      author='Michael, Nick, Sahj, Torren',
      packages=['security_simulation'],
      install_requires=[
          'numpy'
      ],
      tests_require=[
          'pytest'
      ],
      zip_safe=False)
