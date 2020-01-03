import absl
import tensorflow as tf


def model_builder_multiclass_classification(model, optimizer=None, metrics=None):
    optimizer = optimizer or tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, amsgrad=False)
    metrics = metrics or [tf.keras.metrics.CategoricalAccuracy(name='accuracy')]
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=metrics)
    absl.logging.info(model.summary())
    return model
