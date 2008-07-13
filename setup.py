try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='BlueChips',
    version='',
    description='BlueChips - finances for people with shared expenses',
    author='Residents of Blue Sun Corporate Headquarters',
    author_email='chips@blue-sun-corp.com',
    #url='',
    install_requires=["Pylons>=0.9.6", "SQLAlchemy>=0.4.1", "tw.forms>=0.9.1"],
    setup_requires=["PasteScript==dev,>=1.6.3dev-r7326"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'bluechips': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors = {'bluechips': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', None),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = bluechips.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
