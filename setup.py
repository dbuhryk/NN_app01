import os
from setuptools import setup


setup(name='NNApp01',
      version='0.1.0',
      description='NN Programming Assignment ',
      author='Dzmitry Buhryk',
      author_email='dzmitry.buhryk@gmail.com',
      license='MIT',
      install_requires=['flask', 'werkzeug'],
      tests_require=['requests', 'flask', 'werkzeug', 'urllib3'],
      packages=['app01', 'test'],
      include_package_data=True,
      package_data={
          'app01': ['static/index_t.html', 'resources/Keyword.txt'],
          'test': ['resources/*']
      },
      package_dir={
          'app01': 'app01',
          'test': 'test'
      },
      zip_safe=False)
