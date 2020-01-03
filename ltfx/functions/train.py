import tensorflow as tf
import tensorflow_transform as tft
from functools import partial
from ltfx.models.keras import model_builder_multiclass_classification
from ltfx.models.resnet50 import build_resnet50
from ltfx.functions.input import _input_fn
from ltfx.functions.serving import _serving_receiver_fn
from ltfx.functions.eval import _eval_input_receiver_fn


def _train_fn(trainer_fn_args, schema, **kwargs):

    transform_output = tft.TFTransformOutput(trainer_fn_args.transform_output)

    input_fn = partial(_input_fn, image_key=kwargs['image_key'], label_key=kwargs['label_key'])
    train_input_fn = lambda: input_fn(trainer_fn_args.train_files, transform_output,
                                      batch_size=kwargs['train_batch_size'])

    eval_input_fn = lambda : input_fn(trainer_fn_args.eval_files, transform_output,
                                      batch_size=kwargs['eval_batch_size'])

    train_spec = tf.estimator.TrainSpec(train_input_fn, max_steps=trainer_fn_args.train_steps)

    serving_receiver_fn = partial(_serving_receiver_fn, raw_label_key=kwargs['raw_label_key'],
                                  image_key=kwargs['image_key'], label_key=kwargs['label_key'])
    serving_fn = lambda: serving_receiver_fn(transform_output, schema)
    exporter = tf.estimator.FinalExporter(kwargs['model_name'], serving_fn)

    eval_spec = tf.estimator.EvalSpec(eval_input_fn, steps=trainer_fn_args.eval_steps, exporters=[exporter],
                                      name=kwargs['model_name'])

    run_config = tf.estimator.RunConfig(save_checkpoints_steps=999, keep_checkpoint_max=1)
    run_config = run_config.replace(model_dir=trainer_fn_args.serving_model_dir)

    model = build_resnet50(input_name=kwargs['image_key'],
                           image_height=kwargs['image_height'],
                           image_width=kwargs['image_width'],
                           number_of_classes=kwargs['number_of_classes'],
                           weights=kwargs['pretrained'])
    keras_model = model_builder_multiclass_classification(model)

    estimator = tf.keras.estimator.model_to_estimator(keras_model=keras_model, config=run_config)

    eval_input_receiver_fn = partial(_eval_input_receiver_fn,
                                     image_key=kwargs['image_key'],
                                     label_key=kwargs['label_key'])
    receiver_fn = lambda: eval_input_receiver_fn(transform_output, schema)

    return {
        "estimator": estimator,
        "train_spec": train_spec,
        "eval_spec": eval_spec,
        "eval_input_receiver_fn": receiver_fn
    }