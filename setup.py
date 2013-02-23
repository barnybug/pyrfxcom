from setuptools import setup

__version__ = '0.1.0'
long_description = file('README.md', 'r').read()

setup(name='pyrfxcom',
      version=__version__,
      description='Python library for reading from an rfxcom USB unit',
      long_description=long_description,
      license='MIT',
      author='Barnaby Gray',
      author_email='barnaby@pickle.me.uk',
      url='http://github.com/barnybug/pyrfxcom/',
      packages=['rfxcom'],
      install_requires=[],
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        ],
      )
