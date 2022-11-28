from setuptools import setup

setup(
    name='github',
    version='0.0.2',
    py_modules=['github_cli'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'github = github_cli:cli',
        ],
    },
)
