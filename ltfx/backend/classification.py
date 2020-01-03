import tensorflow as tf
from ltfx.common import ClassificationConfig
from ltfx.preprocessing.image import read_tensor_from_image_file
from ltfx.preprocessing.label import label_to_one_hot
from ltfx.functions.train import _train_fn
from functools import partial


def preprocessing_fn(inputs):
    config = ClassificationConfig.from_env()

    outputs = dict()
    read_tensor = partial(read_tensor_from_image_file, input_height=config.image_height, input_width=config.image_width)

    outputs[config.image_key] = tf.compat.v2.map_fn(read_tensor, inputs[config.raw_image_key].values, dtype=tf.float32)

    one_hot = partial(label_to_one_hot, size=config.number_of_classes)
    outputs[config.label_key] = tf.compat.v2.map_fn(one_hot, inputs[config.raw_label_key].values, dtype=tf.float32)

    return outputs


def trainer_fn(hparams, schema):
    config = ClassificationConfig.from_env()

    return _train_fn(hparams, schema,
                     image_key=config.image_key,
                     label_key=config.label_key,
                     raw_label_key=config.raw_label_key,
                     model_name=config.model_name,
                     image_height=config.image_height,
                     image_width=config.image_width,
                     number_of_classes=config.number_of_classes,
                     pretrained=config.pretrained,
                     train_batch_size=config.train_batch_size,
                     eval_batch_size=config.eval_batch_size)
