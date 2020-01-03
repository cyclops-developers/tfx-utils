#!/usr/bin/env python3
# coding=utf-8

from __future__ import print_function

import os
import click
from importlib.machinery import SourceFileLoader
from inspect import getmembers
from absl import logging
from .test import cli as cli_test
from .workflow import cli as cli_workflow
from .server import cli as cli_server


logger = logging.get_absl_logger()

__all__ = ['create_cli']


def load_commands_from_file(path):
    module = SourceFileLoader('custom_commands', path).load_module()
    commands = [obj for name, obj in getmembers(module) if isinstance(obj, click.core.Command)]
    return commands


def create_cli(package_name, package_path, exclude=None, type_=None, config=None):
    base_path = os.path.abspath(os.path.join(package_path, '..'))

    @click.group('custom')
    @click.option('--debug', is_flag=True, help='Enable debug mode.')
    @click.pass_context
    def cli(ctx, debug):
        ctx.obj = {
            'debug': debug,
            'package_name': package_name,
            'package_path': package_path,
            'base_path': base_path,
            'type': type_,
            'config': config,
        }

    commands = {}
    commands.update(cli_test.commands)
    commands.update(cli_workflow.commands)
    commands.update(cli_server.commands)
    for name, command in commands.items():
        cli.add_command(command, name=name)

    commands_file_path = os.path.join(base_path, 'commands.py')
    logger.info(commands_file_path)
    if os.path.exists(commands_file_path):
        commands = load_commands_from_file(commands_file_path)
        for command in commands:
            cli.add_command(command)

    return cli
