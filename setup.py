# setup.py

from setuptools import setup, find_packages

setup(
    name='ai_coding',
    version='0.1.0',
    author='Guokai Ma',
    author_email='guokai.ma@gmail.com',
    description='ai_coding is a python package for AI coding.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/delock/ai_coding',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
    install_requires=[
        # Add any dependencies here
    ],
    entry_points={
        'console_scripts': [
            'ai_coding=ai_coding.ai_coding:main',
        ],
    },
)
