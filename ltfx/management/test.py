from __future__ import print_function

import sys
import os
import os.path
import subprocess
import click


__all__ = ['create_cli']


@click.group('test')
def cli():
    pass


@cli.command('test', help='Run tests located in tests folder.')
@click.pass_context
def test(ctx,):
    os.environ['TESTING'] = 'true'
    command = ['python', '-m', 'unittest']
    cwd = os.path.join(ctx.obj['base_path'])
    print(' '.join(command))
    exitcode = subprocess.call(command, cwd=cwd)
    sys.exit(exitcode)
