from __future__ import print_function
import os
import sys
import click
import subprocess


__all__ = ['create_cli']


@click.group('server')
def cli():
    pass


@cli.command('notebook', help='Start the Jupyter notebook server.')
@click.option('--port', '-p', default=8888, help='Jupyter server port')
@click.pass_context
def notebook(ctx, port):
    notebookdir = os.path.join(ctx.obj['package_path'], '..', 'notebooks')
    command = [
        'jupyter', 'notebook',
        '--notebook-dir', notebookdir,
        '--ip', '0.0.0.0',
        '--port', str(port),
        '--no-browser',
    ]
    ret = os.system(' '.join(command))
    sys.exit(ret)


@cli.command('runserver', help='Start the server.')
@click.option('--model_name', '-m', default='model', help='Model name')
@click.option('--grpc_port', '-g', default=8500, help='Server gRPC port')
@click.option('--http_port', '-p', default=8501, help='Server http port')
@click.option('--credentials_json', '-c', default=None, help='GCP Credentials JSON - GOOGLE_APPLICATION_CREDENTIALS')
@click.pass_context
def runserver(ctx, model_name, grpc_port, http_port, credentials_json):
    model_on_disk = os.path.abspath(os.path.join(ctx.obj['package_path'], '..', 'dist'))
    if os.path.exists(model_on_disk) and os.path.isdir(model_on_disk) and os.listdir(model_on_disk):
        bind = "type=bind,source={}/,target=/models/{}".format(model_on_disk, model_name)
        if credentials_json is None:
            command = ["docker", "run",
                       "-p", "%d:8500" % grpc_port,
                       "-p", "%d:8501" % http_port,
                       "--mount", bind,
                       "-e", "MODEL_NAME=%s" % model_name,
                       "-t", "tensorflow/serving"]
        else:
            credentials_path = os.path.dirname(credentials_json)
            credentials = os.path.join('/opt/credentials', os.path.basename(credentials_json))
            command = ["docker", "run",
                       "-p", "%d:8500" % grpc_port,
                       "-p", "%d:8501" % http_port,
                       "--mount", bind,
                       "-v", "%s:/opt/credentials/" % credentials_path,
                       "-e", "MODEL_NAME=%s" % model_name,
                       "-e", "GOOGLE_APPLICATION_CREDENTIALS=%s" % credentials,
                       "-t", "tensorflow/serving"]
        print(command)
        subprocess.call(command)
    else:
        print("No model found at {}".format(model_on_disk))
