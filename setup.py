from setuptools import setup

from flask_scaffold import __version__


with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='flask-scaffold',
    author='enwawerueli',
    author_email='enwawerueli17@gmail.com',
    version=__version__,
    description='Scaffold a flask app',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/enwawerueli/flask-scaffold',
    packages=['flask_scaffold'],
    include_package_data=True,
    install_requires=['click>=7.0', 'jinja2>=2.10'],
    entry_points=dict(
        console_scripts=[
            'flask-scaffold=flask_scaffold.core:create_app']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Linux',
        'Intended Audience :: Developers',
        'Framework :: Flask',
        'Topic :: Utilities',
        'Natural Language :: English'],
    python_requires='>=3')
