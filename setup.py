from setuptools import setup

from flask_skeleton import __version__

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='flask-skeleton',
    author='enwawerueli',
    author_email='seaworndrift@gmail.com',
    version=__version__,
    description='Quick start a flask app',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/enwawerueli/flask-skeleton',
    packages=['flask_skeleton'],
    include_package_data=True,
    install_requires=['click==7.1.1', 'jinja2==2.11.3'],
    entry_points='''
        [console_scripts]
        create-flask-app=flask_skeleton.core:create_flask_app
    ''',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Intended Audience :: Developers',
        'Framework :: Flask',
        'Topic :: Utilities',
        'Natural Language :: English'],
    python_requires='>=3')
