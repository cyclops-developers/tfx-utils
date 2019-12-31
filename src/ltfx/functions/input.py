import tensorflow as tf
from ltfx.common import gzip_reader_fn, ClassificationConfig


def input_fn(filenames, transform_output, batch_size):
    transformed_feature_spec = transform_output.transformed_feature_spec().copy()
    dataset = tf.data.experimental.make_batched_features_dataset(filenames, batch_size,
                                                                 transformed_feature_spec,
                                                                 reader=gzip_reader_fn)

    transformed_features = tf.compat.v1.data.make_one_shot_iterator(dataset).get_next()
    labels = transformed_features.pop(ClassificationConfig.LABEL_KEY)
    inputs = {ClassificationConfig.IMAGE_KEY: transformed_features[ClassificationConfig.IMAGE_KEY]}
    return inputs, labels
