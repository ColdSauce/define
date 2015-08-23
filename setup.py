from distutils.core import setup

import define

setup(name='define',
      description='Terminal Dictionary',
      long_description=open('README.Md').read(),
      version=define.__version__,
      author='Johnathan "shaggytwodope" Jenkins',
      author_email='twodopeshaggy@gmail.com',
      url='https://github.com/SethDusek/define',
      data_files=[
      ("share/man/man1", ["define.1"])
      ],
      scripts=['define'],
      requires=['wordnik', 'requests'],
      classifiers=['Intended Audience :: End Users/Desktop',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3'],
      license='BSD')
