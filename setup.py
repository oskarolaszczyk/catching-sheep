# from distutils.core import setup
# # TODO setuptools - rozwazyc
#
# setup(name='chase',
#       version='1.0',
#       author="Oskar Olaszczyk",
#       author_email=" TUL email: 224389@edu.pl, personal email: oskarolaszczyk@gmail.com",
#       license="MIT",
#       description="simple sheep catching by wolf simulation",
#       packages=['chase'],
#       )

import setuptools

setuptools.setup(
      name='chase',
      version='1.0',
      author="Oskar Olaszczyk",
      author_email=" TUL email: 224389@edu.pl, personal email: oskarolaszczyk@gmail.com",
      license="MIT",
      description="simple sheep catching by wolf simulation",
      install_requires=['scipy', 'colorama'],
      packages=['chase'],
      )