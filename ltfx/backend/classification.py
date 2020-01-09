import tensorflow as tf
import tensorflow_transform as tft
from absl import logging
from ltfx.common import ClassificationConfig
from ltfx.preprocessing.image import read_tensor_from_image_file
from ltfx.functions.train import _train_fn


def preprocessing_fn(inputs):
    logging.info("Running preprocessing function")

    config = ClassificationConfig.from_env()

    outputs = dict()
    read_image_blob = lambda x: read_tensor_from_image_file(x,
                                                            input_height=config.image_height,
                                                            input_width=config.image_width)
    # image tensor
    outputs[config.image_key] = tf.compat.v2.map_fn(read_image_blob,
                                                    inputs[config.raw_image_key].values,
                                                    dtype=tf.float32)
    # label tensor
    # we store input to output and create a vocabulary to be used later on
    _ = tft.vocabulary(inputs['label'], vocab_filename="label_encoder")
    outputs[config.label_key] = inputs[config.raw_label_key]

    return outputs


def trainer_fn(hparams, schema):
    logging.info("Running trainer function")

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
