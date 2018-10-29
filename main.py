#!/usr/bin/env python

import os
import shutil
import platform
import venv
import subprocess

import click
import jinja2 as j2


cwd = os.getcwd()
root = os.path.dirname(os.path.realpath(__file__))
src = os.path.join(root, 'scafold')

jinja_env = j2.Environment(loader=j2.FileSystemLoader(root))


@click.command()
@click.argument('appname')
@click.option('-d', '--dest', default=None, type=click.Path(exists=True, writable=True),
              help=('The destination path of your app. '
                    'Defaults to a directory named [APPNAME] in the current directory.'))
@click.option('-e', '--virtual-environment', 'env', is_flag=True, help='Create virtual environment.')
@click.option('-g', '--git', is_flag=True, help='Initialize git repository.')
def create_app(appname, dest, env, git):
    """Scaffold a new Flask application."""
    dest = os.path.realpath(os.path.join(cwd if dest is None else dest, appname))
    try:
        template = jinja_env.get_template('summary.jinja2')
    except j2.TemplateNotFound:
        pass
    else:
        click.echo(template.render(appname=appname, path=dest, py_version=platform.python_version(),
                                   venv=env, git=git))
        click.confirm('Continue with these settings?', abort=True)
    if os.path.exists(dest) is True:
        click.confirm('The destination already exists. Overwrite?', abort=True)
        shutil.rmtree(dest)
    click.echo('Copying files...')
    shutil.copytree(src, dest)
    click.echo('done!')
    env_dir = os.path.join(dest, 'venv')
    if env is True:
        click.echo('Creating virtual environment...')
        try:
            venv.create(env_dir, with_pip=True)
        except Exception:
            click.echo('A problem occured while creating virtual environment...Ignoring.')
            if os.path.exists(env_dir):
                shutil.rmtree(env_dir)
        else:
            click.echo('done!')
    if git is True:
        click.echo('Initializing git repository...')
        git = shutil.which('git')
        if git is None:
            click.echo('Failed to find git executable...Ignoring.')
        else:
            try:
                subprocess.run([git, 'init', dest], check=True)
            except Exception:
                click.echo('A problem occured while Initializing git repository...Ignoring.')
                repo = os.path.join(dest, '.git')
                if os.path.exists(repo):
                    shutil.rmtree(repo)
            else:
                with open(os.path.join(dest, '.gitignore'), 'w') as f:
                    f.write('# Ignored files and directories\n')
                    if os.path.exists(env_dir):
                        f.write('venv/\n')
                subprocess.run(['git', 'add', '.'])
                subprocess.run(['git', 'commit', '-m', '"Creates app skeleton."'])
                click.echo('done!')


if __name__ == '__main__':
    create_app()
