# coding=utf-8
from setuptools import setup, find_packages

setup(
    name="ibe",
    version='0.1',
    url='https://github.com/mschuetz/imageblog-editor',
    author='Matthias Schütz',
    author_email='mschuetz@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(exclude=["contrib", "docs", "test*"]),
    install_requires=['Flask'],
    package_data={
        'ibe': ['static/bootstrap/css/*', 'static/zepto*', 'templates/*']
    },
    entry_points={
        'console_scripts': [
            'ibe=ibe:main',
        ],
    },
)
