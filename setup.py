from setuptools import setup

setup(
    name='github',
    version='0.0.1',
    py_modules=['main'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'github = main:cli',
        ],
    },
)
