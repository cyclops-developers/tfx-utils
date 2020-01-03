import tensorflow as tf
from tensorflow_transform.tf_metadata import schema_utils


def get_raw_feature_spec(schema):
    return schema_utils.schema_as_feature_spec(schema).feature_spec


def gzip_reader_fn(filenames):
    return tf.data.TFRecordDataset(filenames, compression_type='GZIP')
