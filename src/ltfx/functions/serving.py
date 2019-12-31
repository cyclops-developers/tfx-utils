import tensorflow as tf
from ltfx.common import get_raw_feature_spec, ClassificationConfig


def serving_receiver_fn(transform_output, schema):
    feature_spec = get_raw_feature_spec(schema)
    feature_spec.pop(ClassificationConfig.RAW_LABEL_KEY)

    input_fn = tf.estimator.export.build_parsing_serving_input_receiver_fn(feature_spec, default_batch_size=None)
    serving_input_receiver = input_fn()

    transformed_features = transform_output.transform_raw_features(serving_input_receiver.features)
    transformed_features.pop(ClassificationConfig.LABEL_KEY)
    inputs = {ClassificationConfig.IMAGE_KEY: transformed_features[ClassificationConfig.IMAGE_KEY]}

    return tf.estimator.export.ServingInputReceiver(inputs, serving_input_receiver.receiver_tensors)
