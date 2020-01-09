import tensorflow as tf
import tensorflow_transform as tft
from tensorflow.python.ops import lookup_ops
from ltfx.models.resnet50 import build_resnet50
from ltfx.functions.input import _input_fn
from ltfx.functions.serving import _serving_receiver_fn
from ltfx.functions.eval import _eval_input_receiver_fn


def _train_fn(trainer_fn_args, schema, **kwargs):

    transform_output = tft.TFTransformOutput(trainer_fn_args.transform_output)
    vocabulary = transform_output.vocabulary_by_name('label_encoder')

    input_fn = lambda: _input_fn(trainer_fn_args.train_files, transform_output,
                                 kwargs['train_batch_size'],
                                 kwargs['image_key'],
                                 kwargs['label_key'])

    eval_fn = lambda : _input_fn(trainer_fn_args.eval_files, transform_output,
                                 kwargs['eval_batch_size'],
                                 kwargs['image_key'],
                                 kwargs['label_key'])

    train_spec = tf.estimator.TrainSpec(input_fn, max_steps=trainer_fn_args.train_steps)

    serving_fn = lambda: _serving_receiver_fn(transform_output, schema,
                                              kwargs['raw_label_key'],
                                              kwargs['image_key'],
                                              kwargs['label_key'])
    exporter = tf.estimator.FinalExporter(kwargs['model_name'], serving_fn)

    eval_spec = tf.estimator.EvalSpec(eval_fn,
                                      steps=trainer_fn_args.eval_steps,
                                      exporters=[exporter],
                                      name=kwargs['model_name'])

    def model_fn(features, labels, mode):
        model = build_resnet50(kwargs['image_key'],
                               image_height=kwargs['image_height'],
                               image_width=kwargs['image_width'],
                               number_of_classes=len(vocabulary),
                               weights=kwargs['pretrained'])
        logits = model(features, training=False)

        class_ids = tf.cast(tf.sort(tf.argsort(logits, axis=1)), tf.int64)
        classes = lookup_ops.index_to_string_table_from_tensor(vocabulary_list=tuple(vocabulary),
                                                               name='class_string_lookup').lookup(class_ids)
        predictions = {
            'probabilities': tf.nn.softmax(logits),
            'class_id': classes,
            'logits': logits,
        }

        if mode == tf.estimator.ModeKeys.PREDICT:
            return tf.estimator.EstimatorSpec(mode=mode,
                                              predictions=predictions)

        label_ids = lookup_ops.index_table_from_tensor(vocabulary_list=tuple(vocabulary),
                                                       name='class_id_lookup').lookup(labels)

        optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=.001)
        loss = tf.keras.losses.CategoricalCrossentropy(from_logits=True,
                                                       reduction=tf.keras.losses.Reduction.NONE)(label_ids, logits)
        loss = tf.reduce_sum(loss) * (1. / 4)

        mean = tf.compat.v1.metrics.mean(loss)
        accuracy = tf.compat.v1.metrics.accuracy(class_ids, label_ids)
        tf.summary.scalar('accuracy', accuracy[1])

        eval_metric_ops = {"accuracy": accuracy, "mean": mean}

        train_op = optimizer.minimize(loss, tf.compat.v1.train.get_or_create_global_step())

        if mode == tf.estimator.ModeKeys.EVAL:
            return tf.estimator.EstimatorSpec(mode=mode,
                                              predictions=predictions,
                                              loss=loss,
                                              eval_metric_ops=eval_metric_ops)

        return tf.estimator.EstimatorSpec(
            mode=mode,
            loss=loss,
            train_op=train_op,
            predictions=predictions,
            eval_metric_ops=eval_metric_ops)

    run_config = tf.estimator.RunConfig(save_checkpoints_steps=999, keep_checkpoint_max=1)
    run_config = run_config.replace(model_dir=trainer_fn_args.serving_model_dir)

    estimator = tf.estimator.Estimator(model_fn=model_fn, config=run_config)

    receiver_fn = lambda: _eval_input_receiver_fn(transform_output, schema, kwargs['image_key'], kwargs['label_key'])

    return {
        "estimator": estimator,
        "train_spec": train_spec,
        "eval_spec": eval_spec,
        "eval_input_receiver_fn": receiver_fn
    }