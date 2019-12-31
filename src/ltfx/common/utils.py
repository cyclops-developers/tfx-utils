import tensorflow as tf
import tempfile
from tensorflow_transform.tf_metadata import schema_utils
from jinja2 import Template


def get_raw_feature_spec(schema):
    return schema_utils.schema_as_feature_spec(schema).feature_spec


def gzip_reader_fn(filenames):
    return tf.data.TFRecordDataset(filenames, compression_type='GZIP')


def render_templates(config_template, config):
    with open(config_template, 'r') as fp:
        template = "".join(fp.readlines())
    tm = Template(template)
    content = tm.render(**config)

    tmpfile = tempfile.NamedTemporaryFile(suffix='.py', delete=False)
    with open(tmpfile.name, 'w') as fp:
        fp.write(content)

    return tmpfile.name

