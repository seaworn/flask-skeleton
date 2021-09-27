import os
import sys
import shutil
import platform
import subprocess
import secrets

import click
import jinja2

from . import __version__

src = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skeleton')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(os.path.abspath(__file__))))


@click.command()
@click.argument('app_name', type=click.STRING)
@click.option(
	'-d', '--dir', default=None, type=click.Path(exists=True, writable=True),
    help='Where to create your app. Defaults to the current directory.')
@click.option('-e', '--env', is_flag=True, help='Create a virtual environment.')
@click.option('-g', '--git', is_flag=True, help='Initialize a git repository.')
@click.version_option(__version__, '-V', '--version')
@click.help_option('-h', '--help')
def create_flask_app(app_name, dir, env, git):
    """Create a flask app skeleton."""
    dest = os.path.abspath(os.path.join(os.getcwd() if dir is None else dir, app_name))
    try:
        summary = jinja_env.get_template('summary.jinja')
    except jinja2.TemplateNotFound:
        pass
    else:
        click.echo(summary.render(dict(
            app_name=app_name,
            path=dest,
            version=platform.python_version(),
            env=env,
            git=git)))
        click.confirm('Continue with these settings?', abort=True)
    if os.path.exists(dest):
        click.confirm('The destination already exists. Overwrite?', abort=True)
        shutil.rmtree(dest)
    click.echo('Copying files...')
    shutil.copytree(src, dest)
    with open(os.path.join(dest, ".env"), "a") as f:
        f.writelines(["\n", "SECRET_KEY=%s" % secrets.token_hex(32)])
    if env is True:
        create_env(dest)
    if git is True:
        init_git_repo(dest)
    click.echo('Done! App created in: %s' % dest)


def create_env(dest, env_name='env'):
    """
    Create a virtual environment.
    :param dest: The full path to the project root.
    """
    click.echo('Creating a virtual environment...')
    virtualenv = shutil.which('virtualenv')
    if virtualenv is None:
        click.echo('Failed to find virtualenv executable...Skipping!')
        return False
    env_path = os.path.join(dest, env_name)
    try:
        subprocess.run([virtualenv, '--python=%s' % sys.executable, env_path], check=True)
    except subprocess.SubprocessError:
        shutil.rmtree(env_path)
        click.echo('A problem occured whith virtualenv...Skipping!')
        return False
    with open(os.path.join(dest, '.gitignore'), 'a') as f:
        f.writelines(['\n', '%s/' % os.path.basename(env_path)])
    click.echo('Installing packages...')
    pip = os.path.join(env_path, 'bin/pip')
    requirements = os.path.join(dest, 'requirements.txt')
    try:
        subprocess.run([pip, 'install', '-r', requirements], check=True)
        subprocess.run([pip, 'freeze', '>', requirements], check=True)
    except subprocess.SubprocessError:
        click.echo('A problem occurred with pip...Skipping!')
        return False
    else:
        return True

    
def init_git_repo(dest):
    """
    Initialize a git repository.
    :param dest: The full path to the project root.
    """
    click.echo('Initializing git repository...')
    git = shutil.which('git')
    if git is None:
        click.echo('Failed to find git executable...Skipping!')
        return False
    os.environ['GIT_WORK_TREE'] = dest
    os.environ['GIT_DIR'] = os.path.join(dest, '.git')
    try:
        subprocess.run([git, 'init'], check=True)
        click.echo('Committing changes...')
        subprocess.run([git, 'add', dest], check=True)
        subprocess.run([git, 'commit', '-m', '"Creates app skeleton."'], check=True)
        subprocess.run([git, 'checkout', '-b', 'devel'], check=True)
    except subprocess.SubprocessError:
        click.echo('A problem occurred whith git...Skipping!')
        return False
    else:
        return True
