#!/usr/bin/python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='BlueChips',
    version='1.0.4',
    description='BlueChips - finances for people with shared expenses',
    long_description=open('README.rst').read(),
    author='Residents of Blue Sun Corporate Headquarters',
    author_email='chips@blue-sun-corp.com',
    url='http://github.com/ebroder/bluechips',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Pylons',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Topic :: Home Automation',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Office/Business :: Financial :: Accounting',
        ],
    install_requires=["Pylons>=0.9.6",
                      "WebHelpers>=1.0a",
                      "SQLAlchemy>=0.5",
                      "AuthKit>=0.4.0",
                      "FormEncode>=1.2.1",
                      "mailer>=0.5"],
    setup_requires=["PasteScript==dev,>=1.6.3dev-r7326"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = bluechips.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
