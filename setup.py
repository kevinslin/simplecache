from distutils.core import setup

PACKAGE = 'simplecache'
NAME = 'simplecache'
DESCRIPTION = 'simple persistent caching even after program termination'
AUTHOR = "Kevin S  Lin"
AUTHOR_EMAIL = "kevinslin8@gmail.com"
URL = "kevinslin.com"
VERSION = __import__(PACKAGE).__version__

setup(name='simplecache',
        version='0.0.1',
        description = DESCRIPTION,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        long_description = '', #TODO
        packages = ['simplecache'],
        )

