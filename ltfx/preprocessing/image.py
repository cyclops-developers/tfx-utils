import tensorflow as tf


def read_tensor_from_image_file(file_name, input_height, input_width, input_mean=0, input_std=255):
    blob = tf.compat.v1.read_file(tf.squeeze(file_name), "reader")
    image = tf.image.decode_jpeg(blob, channels=3, name="decoder")
    image = tf.cast(image, tf.float32)
    image = tf.image.resize_with_pad(image, target_height=input_height, target_width=input_width)
    image = tf.divide(tf.subtract(image, [input_mean]), [input_std])
    return image
