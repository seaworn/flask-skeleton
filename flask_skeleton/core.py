#!/usr/bin/env python

import os
import shutil
import platform
import venv
import subprocess as sp

import click
import jinja2 as j2

from . import __version__


src = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skeleton')

jinja_env = j2.Environment(loader=j2.PackageLoader('flask_skeleton'))


@click.command()
@click.argument('appname')
@click.option('-d', '--dest', default=None, type=click.Path(exists=True, writable=True),
              help='Where to create your app. Defaults to the current directory.')
@click.option('-v', '--virtualenv', is_flag=True, help='Create a virtual environment.')
@click.option('-g', '--git', is_flag=True, help='Initialize a git repository.')
@click.version_option(__version__, '-V', '--version')
@click.help_option('-h', '--help')
def create_flask_app(appname, dest, virtualenv, git):
    """Create a flask app skeleton."""

    dest = os.path.abspath(
        os.path.join(os.getcwd() if dest is None else dest, appname))
    try:
        summary = jinja_env.get_template('summary.jinja2')
    except j2.TemplateNotFound:
        pass
    else:
        context = dict(
            appname=appname,
            path=dest,
            python_version=platform.python_version(),
            virtualenv=virtualenv,
            git=git
        )
        click.echo(summary.render(context))
        click.confirm('Continue with these settings?', abort=True)
    if os.path.exists(dest):
        click.confirm('The destination already exists. Overwrite?', abort=True)
        shutil.rmtree(dest)
    click.echo('Copying files...')
    shutil.copytree(src, dest)
    if virtualenv is True:
        create_virtualenv(dest)
    if git is True:
        create_git_repo(dest)
    click.echo('Done!\n' 'New app created in %s' % dest)


def create_virtualenv(dest):
    """Create a virtual environment
    :param dest: full path to the project root
    """

    click.echo('Creating virtual environment...')
    env_dir = os.path.join(dest, 'venv')
    try:
        venv.create(env_dir, with_pip=True)
    except Exception:
        click.echo('A problem occured whith venv...Skipping!')
        return False
    with open(os.path.join(dest, '.gitignore'), 'a') as f:
        f.write('%s/' % os.path.basename(env_dir))
    click.echo('Installing packages...')
    pip_exe = os.path.join(env_dir, 'bin/pip')
    reqr = os.path.join(dest, 'requirements.txt')
    try:
        sp.run([pip_exe, 'install', '-r', reqr], check=True)
        sp.run([pip_exe, 'freeze', '>', reqr], check=True)
    except sp.SubprocessError:
        click.echo('A problem occurred with pip...Skipping!')
        return False
    return True


def create_git_repo(dest):
    """Initialize a git repository
    :param dest: full path to the project root
    """

    click.echo('Initializing git repository...')
    git_exe = shutil.which('git')
    if git_exe is None:
        click.echo('Failed to find git executable...Skipping!')
        return False
    os.environ['GIT_WORK_TREE'] = dest
    os.environ['GIT_DIR'] = os.path.join(dest, '.git')
    try:
        sp.run([git_exe, 'init'], check=True)
        click.echo('Committing changes...')
        sp.run([git_exe, 'add', dest], check=True)
        sp.run([git_exe, 'commit', '-m', '"Creates app skeleton."'], check=True)
        sp.run([git_exe, 'checkout', '-b', 'devel'], check=True)
    except sp.SubprocessError:
        click.echo('A problem occurred whith git...Skipping!')
        return False
    return True
