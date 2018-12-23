#!/user/bin/env python

import click

from app import create_app, db, models, forms

app = create_app()


# flask cli context
@app.shell_context_processor
def get_context():
    """Expose objects that will be automatically available from the shell"""
    return dict(app=app, db=db, models=models, forms=forms)


@app.cli.command()
def create_db():
    """Create database tables"""
    db.create_all()


@app.cli.command()
@click.confirmation_option(prompt='Drop all database tables?')
def drop_db():
    """Drops database tables."""
    db.drop_all()


if __name__ == '__main__':
    app.run()
