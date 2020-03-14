import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='drf-app-generators',
    version='0.0.2',

    description='Generate DRF Serializers, Views, Apis, Unit tests for your application.',
    long_description=README,

    url='https://github.com/tranquochuy/drf-app-generators.git',
    download_url = 'https://github.com/tranquochuy/drf-app-generators.git',
    author='Huy Tran',
    author_email='huy.tranquoc@asnet.com.vn',

    license='MIT',

    packages=['drf_app_generators', 'drf_app_generators.templates', 'drf_app_generators.management', 'drf_app_generators.management.commands'],
    include_package_data=True,
    install_requires=[
        'Django>=3.0.3',
        'djangorestframework>=3.11.0'
    ],

    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
    ],

    keywords='API REST framework generate scaffold',
)
