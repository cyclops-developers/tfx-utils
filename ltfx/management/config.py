# coding=utf-8

from __future__ import print_function

import os
import os.path
import copy
import logging
from configparser import ConfigParser


__all__ = ['find_inidir', 'parse_ini']


logger = logging.getLogger()


def find_inidir(inifilename='ltfx.ini'):
    inidir = None
    currentdir = os.getcwd()

    while True:
        logger.debug('Looking for ltfx.ini in {}'.format(currentdir))
        if os.path.exists(os.path.join(currentdir, inifilename)):
            inidir = currentdir
            logger.debug('tfx.ini found {}'.format(inidir))
            break

        parentdir = os.path.abspath(os.path.join(currentdir, os.pardir))
        if currentdir == parentdir:
            # currentdir is '/'
            logger.debug('tfx.ini not found')
            break

        currentdir = parentdir

    return inidir


def parse_ini(inipath, defaults=None):
    if defaults is None:
        defaults = {}

    logger.debug("Parsing tfx.ini '{}' with defaults '{}'".format(inipath,
                                                                   defaults))

    config_raw = ConfigParser()
    config_raw.read(inipath)

    config = copy.deepcopy(defaults)

    for section in config_raw.sections():
        # Firt pass
        for key, value in config_raw.items(section):
            key = '_'.join((section, key)).lower()
            logger.debug('Processing {}: {}'.format(key, value))
            processed_value = value.format(**config)
            config[key] = processed_value

    # Second pass
    for key, value in config.items():
        processed_value = value.format(**config)
        if ',' in processed_value:
            processed_value = processed_value.split(',')
        config[key] = processed_value

    logger.debug('tfx.ini loaded: {}'.format(config))

    return config
