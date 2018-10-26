#!/usr/bin/env python

import os
import shutil
import platform

import click
import jinja2 as j2


cwd = os.getcwd()
root = os.path.dirname(os.path.realpath(__file__))
src = os.path.join(root, 'scafold')

jinja_env = j2.Environment(loader=j2.FileSystemLoader(root))


@click.command()
@click.argument('appname')
@click.option('-d', '--dest', default=None,
              help=('The destination path of your app. '
                    'Defaults to a directory named [APPNAME] in the current directory'))
def create_app(appname, dest):
    """Scaffold a new Flask application."""
    dest = os.path.realpath(os.path.join(cwd, appname) if dest is None else dest)
    try:
        template = jinja_env.get_template('summary.jinja2')
    except j2.TemplateNotFound:
        pass
    else:
        click.echo(template.render(appname=appname, path=dest, py_version=platform.python_version()))
        click.confirm('Continue with these settings?', abort=True)
    if os.path.exists(dest) is True:
        click.confirm('The destination already exists. Overwrite?', abort=True)
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


if __name__ == '__main__':
    create_app()
