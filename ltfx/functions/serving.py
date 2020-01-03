import tensorflow as tf
from ltfx.common import get_raw_feature_spec


def _serving_receiver_fn(transform_output, schema, raw_label_key, image_key, label_key):
    feature_spec = get_raw_feature_spec(schema)
    feature_spec.pop(raw_label_key)

    input_fn = tf.estimator.export.build_parsing_serving_input_receiver_fn(feature_spec, default_batch_size=None)
    serving_input_receiver = input_fn()

    transformed_features = transform_output.transform_raw_features(serving_input_receiver.features)
    transformed_features.pop(label_key)
    inputs = {image_key: transformed_features[image_key]}

    return tf.estimator.export.ServingInputReceiver(inputs, serving_input_receiver.receiver_tensors)
