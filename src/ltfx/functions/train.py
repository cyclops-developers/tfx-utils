import tensorflow as tf
import tensorflow_transform as tft
from ltfx.models.keras import keras_model_builder_multiclass_classification
from ltfx.models.resnet50 import build_resnet50
from ltfx.functions.input import input_fn
from ltfx.functions.serving import serving_receiver_fn
from ltfx.functions.eval import eval_input_receiver_fn


def train_fn(trainer_fn_args, schema, model_name, height, width, n_classes,
             train_batch_size, eval_batch_size, *args, **kwargs):

    transform_output = tft.TFTransformOutput(trainer_fn_args.transform_output)

    train_input_fn = lambda: input_fn(trainer_fn_args.train_files, transform_output, batch_size=train_batch_size)
    eval_input_fn = lambda : input_fn(trainer_fn_args.eval_files, transform_output, batch_size=eval_batch_size)

    train_spec = tf.estimator.TrainSpec(train_input_fn, max_steps=trainer_fn_args.train_steps)

    serving_fn = lambda: serving_receiver_fn(transform_output, schema)
    exporter = tf.estimator.FinalExporter(model_name, serving_fn)

    eval_spec = tf.estimator.EvalSpec(eval_input_fn, steps=trainer_fn_args.eval_steps, exporters=[exporter],
                                      name=model_name)

    run_config = tf.estimator.RunConfig(save_checkpoints_steps=999, keep_checkpoint_max=1)
    run_config = run_config.replace(model_dir=trainer_fn_args.serving_model_dir)

    keras_model = keras_model_builder_multiclass_classification(build_resnet50(height, width, n_classes))
    estimator = tf.keras.estimator.model_to_estimator(keras_model=keras_model,
                                                      config=run_config)

    receiver_fn = lambda: eval_input_receiver_fn(transform_output, schema)

    return {
        "estimator": estimator,
        "train_spec": train_spec,
        "eval_spec": eval_spec,
        "eval_input_receiver_fn": receiver_fn
    }