#!/usr/bin/env python3
# coding=utf-8

import os.path
from ltfx.management import create_cli


package_name = 'ltfx'
package_path = os.path.join(os.path.dirname(__file__), package_name)

cli = create_cli(package_name, package_path)

if __name__ == "__main__":
    cli()
