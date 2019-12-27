import tensorflow as tf
import tensorflow_model_analysis as tfma
from ltfx.common import get_raw_feature_spec, transform_name, ClassificationConfig


def eval_input_receiver_fn(transform_output, schema):
    feature_spec = get_raw_feature_spec(schema)

    serialized_tf_example = tf.compat.v1.placeholder(dtype=tf.string, shape=[None], name='input_example_tensor')

    features = tf.io.parse_example(serialized=serialized_tf_example, features=feature_spec)

    transformed_features = transform_output.transform_raw_features(features)
    labels = transformed_features.pop(ClassificationConfig.LABEL_KEY)
    inputs = {ClassificationConfig.IMAGE_KEY: transformed_features[ClassificationConfig.IMAGE_KEY]}

    receiver_tensors = {'examples': serialized_tf_example}

    return tfma.export.EvalInputReceiver(features=inputs, receiver_tensors=receiver_tensors, labels=labels)
