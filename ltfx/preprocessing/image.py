import tensorflow as tf


def read_tensor_from_image_file(filename, input_height, input_width, input_mean=0, input_std=255):
    blob = tf.io.read_file(filename)
    image = tf.image.decode_image(blob, channels=3)
    image = tf.cast(image, tf.float32)
    image = tf.image.resize_with_pad(image, target_height=input_height, target_width=input_width)
    image = tf.divide(tf.subtract(image, [input_mean]), [input_std])
    return tf.reshape(image, [input_height, input_width, 3])
