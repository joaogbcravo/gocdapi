from setuptools import setup
import os

PROJECT_ROOT, _ = os.path.split(__file__)
REVISION = '1.0.3'
PROJECT_NAME = 'gocdapi'
PROJECT_AUTHORS = "Joao Cravo"
# Please see readme.rst for a complete list of contributors
PROJECT_EMAILS = 'joaogbcravo@gmail.com'

SHORT_DESCRIPTION = 'A Python API for accessing resources on a Go continuous-delivery server.'

try:
    DESCRIPTION = open(os.path.join(PROJECT_ROOT, "README.rst")).read()
except IOError:
    DESCRIPTION = SHORT_DESCRIPTION

GLOBAL_ENTRY_POINTS = {
    "console_scripts": ["go_invoke=gocdapi.command_line.gocdapi_invoke:main",
                        "gocdapi_version=gocdapi.command_line.gocdapi_version:main"]
}

setup(
    name=PROJECT_NAME.lower(),
    version=REVISION,
    author=PROJECT_AUTHORS,
    author_email=PROJECT_EMAILS,
    packages=[
        'gocdapi',
        'gocdapi.command_line',
        'gocdapi.utils',
    ],
    zip_safe=True,
    include_package_data=False,
    install_requires=['requests>=2.3.0'],
    test_suite='nose.collector',
    tests_require=['mock', 'nose', 'coverage', 'nose-testconfig'],
    entry_points=GLOBAL_ENTRY_POINTS,
    description=SHORT_DESCRIPTION,
    long_description=DESCRIPTION,
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
    ],
)
