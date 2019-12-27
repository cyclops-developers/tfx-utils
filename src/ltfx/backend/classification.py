import tensorflow as tf
from ltfx.common import ClassificationConfig, transform_name
from ltfx.preprocessing.image import read_tensor_from_image_file
from ltfx.preprocessing.label import label_to_one_hot
from ltfx.functions.train import train_fn
from functools import partial


def preprocessing_fn(inputs):
    outputs = dict()
    read_tensor = partial(read_tensor_from_image_file,
                          input_height=ClassificationConfig.IMAGE_HEIGHT,
                          input_width=ClassificationConfig.IMAGE_WIDTH)

    outputs[ClassificationConfig.IMAGE_KEY] = tf.compat.v2.map_fn(read_tensor,
                                                                  inputs[ClassificationConfig.RAW_IMAGE_KEY].values,
                                                                  dtype=tf.float32)

    one_hot = partial(label_to_one_hot, size=ClassificationConfig.NUMBER_OF_CLASSES)
    outputs[ClassificationConfig.LABEL_KEY] = tf.compat.v2.map_fn(one_hot,
                                                                  inputs[ClassificationConfig.RAW_LABEL_KEY].values,
                                                                  dtype=tf.float32)

    return outputs


def trainer_fn(hparams, schema):
    return train_fn(hparams, schema,
                    model_name=ClassificationConfig.MODEL_NAME,
                    height=ClassificationConfig.IMAGE_HEIGHT,
                    width=ClassificationConfig.IMAGE_WIDTH,
                    n_classes=ClassificationConfig.NUMBER_OF_CLASSES,
                    train_batch_size=ClassificationConfig.TRAIN_BATCH_SIZE,
                    eval_batch_size=ClassificationConfig.EVAL_BATCH_SIZE)
