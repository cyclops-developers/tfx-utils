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
        if yes or click.confirm('Do you want to edit CHANGELOG.rst?'):
            click.edit(filename=os.path.join(ctx.obj['base_path'], 'CHANGELOG.rst'))
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


@cli.command('run', help='Run pipeline')
@click.option('--config_file', '-c', help='Configuration file', required=True)
@click.pass_context
def run(ctx, config_file):
    command = ['python', os.path.join(ctx.obj['package_path'], '..', 'src', 'pipeline.py'),
               '-c', config_file]
    print(" ".join(command))
    subprocess.call(command)


@cli.command('package', help='Package dependencies to run on GCP')
@click.pass_context
def package(ctx):
    setup = os.path.relpath(os.path.join(os.path.dirname(__file__), '..', '..', 'setup.py'))
    if not os.path.exists(setup):
        print("Could not find setup.py at %s" % setup)
    else:
        command = ['python', setup, 'sdist', '--dist-dir', os.path.join(ctx.obj['package_path'], '..', 'packages')]
        print(" ".join(command))
        subprocess.call(command)


@cli.command('clean', help='Clean previous pipeline execution')
@click.option('--yes', '-y', is_flag=False, help='Answer yes to all prompts')
@click.pass_context
def clean(ctx, yes):
    dist_folder = os.path.relpath(os.path.join(ctx.obj['package_path'], '..', 'dist', '*'))
    command = ['rm', '-rf', dist_folder]
    if yes or click.confirm('Do you want to clean content from %s' % dist_folder):
        print(" ".join(command))
        subprocess.call(command)
    else:
        print("Skip.")
