import tensorflow as tf


def label_to_one_hot(label_id, size):
    label = tf.one_hot(label_id, size)
    return label
