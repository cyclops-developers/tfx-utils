from __future__ import print_function

import os
import sys
import subprocess

import click

__all__ = ['create_cli']


def is_git_clean(path=None):
    if path is None:
        path = os.path.curdir
    command = 'git diff --quiet HEAD'.split()
    exit_code = subprocess.call(command)
    return exit_code == 0


def get_version(path):
    """Return the project version from VERSION file."""
    with open(os.path.join(path, 'VERSION'), 'rb') as f:
        version = f.read().decode('ascii').strip()
    return version.strip()


@click.group('workflow')
def cli():
    pass


@cli.command('bumpversion', help='Bump the package version.')
@click.argument('part', default='patch')
@click.option('--allow-dirty', is_flag=True, help='Allow dirty')
@click.option('--force', '-f', is_flag=True, help='Alias for --allow-dirty')
@click.option('--yes', '-y', is_flag=True, help='Answer yes to all prompts')
@click.pass_context
def bumpversion(ctx, part, allow_dirty, force, yes):
    args = [part]
    allow_dirty = allow_dirty or force

    is_clean = is_git_clean(ctx.obj['base_path'])
    if not is_clean and not allow_dirty:
        print('')
        print('ERROR: Git working directory is not clean.')
        print('')
        print('You can use --allow-dirty or --force if you know what '
              'you\'re doing.')
        exitcode = 1
    else:
        if allow_dirty:
            args.append('--allow-dirty')
        command = ['bumpversion'] + args

        old_version = get_version(ctx.obj['package_path'])
        exitcode = subprocess.call(command, cwd=ctx.obj['base_path'])
        new_version = get_version(ctx.obj['package_path'])

        if exitcode == 0:
            print('Bump version from {old} to {new}'.format(
                old=old_version, new=new_version))
        if yes or click.confirm('Do you want to edit CHANGES.md?'):
            click.edit(filename=os.path.join(ctx.obj['base_path'], 'CHANGES.md'))
    sys.exit(exitcode)


@cli.command('tag', help='Create git tag using the package version.')
@click.pass_context
def tag(ctx):
    tag = 'v{}'.format(get_version(ctx.obj['package_path']))
    print('Creating git tag {}'.format(tag))
    command = ['git', 'tag', '-m', '"version {}"'.format(tag), tag]
    sys.exit(subprocess.call(command))


@cli.command('version', help='Show the package version.')
@click.pass_context
def version(ctx):
    print(get_version(ctx.obj['package_path']))