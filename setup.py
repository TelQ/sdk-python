from setuptools import setup, find_packages

long_decription = ''

with open('readme.MD', 'r') as fh:
    long_decription = fh.read()

setup(
    name='telqsdk',
    version='0.0.1',
    description='TelQ Python SDK',
    long_description=long_decription,
    long_decription_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['requests'],
)
