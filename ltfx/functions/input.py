import tensorflow as tf
from ltfx.common import gzip_reader_fn


def _input_fn(filenames, transform_output, batch_size, image_key, label_key):
    transformed_feature_spec = transform_output.transformed_feature_spec().copy()
    dataset = tf.data.experimental.make_batched_features_dataset(filenames, batch_size,
                                                                 transformed_feature_spec,
                                                                 reader=gzip_reader_fn)

    transformed_features = tf.compat.v1.data.make_one_shot_iterator(dataset).get_next()
    labels = tf.sparse.to_dense(transformed_features.pop(label_key))
    inputs = {image_key: transformed_features[image_key]}
    return inputs, labels
