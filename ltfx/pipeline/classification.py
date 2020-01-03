import os
from absl import logging
from typing import Text
from tfx.components import Evaluator
from tfx.components import CsvExampleGen
from tfx.components import ImporterNode
from tfx.components import ExampleValidator
from tfx.components import ModelValidator
from tfx.components import Pusher
from tfx.components import SchemaGen
from tfx.components import StatisticsGen
from tfx.components import Trainer
from tfx.components import Transform
from tfx.proto import example_gen_pb2
from tfx.proto import evaluator_pb2
from tfx.proto import pusher_pb2
from tfx.proto import trainer_pb2
from tfx.types.standard_artifacts import Schema
from tfx.utils.dsl_utils import external_input
from tfx.orchestration import metadata
from tfx.orchestration import pipeline
from ltfx.common import ClassificationConfig


logger = logging.get_absl_logger()


def create_classification_pipeline(pipeline_name: Text, pipeline_root: Text, data_root: Text, schema_path: Text,
                                   serving_model_dir: Text, metadata_path: Text,
                                   direct_num_workers: int = 0,
                                   config_file: str = None) -> pipeline.Pipeline:

    logger.info("Reading config")
    config = ClassificationConfig.from_file(config_file)

    logger.info("Creating CSV Example component. Data root %s" % data_root)
    examples = external_input(data_root)
    input_config = example_gen_pb2.Input(splits=[
        example_gen_pb2.Input.Split(name='train', pattern='train.csv'),
        example_gen_pb2.Input.Split(name='eval', pattern='eval.csv')
    ])
    example_gen = CsvExampleGen(input=examples, input_config=input_config)

    logger.info("Creating Statistic component")
    statistics_gen = StatisticsGen(examples=example_gen.outputs['examples'])

    logger.info("Creating Schema component")
    schema_gen = SchemaGen(statistics=statistics_gen.outputs['statistics'], infer_feature_shape=False)

    logger.info("Creating Importer Node component. Schema path %s" % schema_path)
    user_schema_importer = ImporterNode(instance_name='custom_schema',
                                        source_uri=schema_path,
                                        artifact_type=Schema)

    logger.info("Creating Example validator component")
    example_validator = ExampleValidator(statistics=statistics_gen.outputs['statistics'],
                                         schema=user_schema_importer.outputs['result'])

    import ltfx.backend.classification
    module_file = ltfx.backend.classification.__file__
    logger.info("Creating Transform component. Backend %s" % module_file)
    transform = Transform(
        examples=example_gen.outputs['examples'],
        schema=user_schema_importer.outputs['result'],
        module_file=os.path.abspath(module_file))

    logger.info("Creating Trainer component. Backend %s" % module_file)
    trainer = Trainer(
      module_file=os.path.abspath(module_file),
      examples=transform.outputs['transformed_examples'],
      schema=user_schema_importer.outputs['result'],
      transform_graph=transform.outputs['transform_graph'],
      train_args=trainer_pb2.TrainArgs(num_steps=config.train_steps),
      eval_args=trainer_pb2.EvalArgs(num_steps=config.eval_steps))

    logger.info("Creating Evaluator component")
    evaluator = Evaluator(
          examples=example_gen.outputs['examples'],
          model_exports=trainer.outputs['model'],
          feature_slicing_spec=evaluator_pb2.FeatureSlicingSpec(
              specs=[evaluator_pb2.SingleSlicingSpec()]))

    logger.info("Creating Model validator component")
    model_validator = ModelValidator(examples=example_gen.outputs['examples'],
                                     model=trainer.outputs['model'])

    logger.info("Creating Pusher component")
    pusher = Pusher(
        model=trainer.outputs['model'],
        model_blessing=model_validator.outputs['blessing'],
        push_destination=pusher_pb2.PushDestination(
            filesystem=pusher_pb2.PushDestination.Filesystem(
                base_directory=serving_model_dir)))

    components = [example_gen, statistics_gen, schema_gen, user_schema_importer, example_validator, transform,
                  trainer, evaluator, model_validator, pusher]

    logger.info("Creating Pipeline")
    return pipeline.Pipeline(
        pipeline_name=pipeline_name,
        pipeline_root=pipeline_root,
        components=components,
        enable_cache=True,
        metadata_connection_config=metadata.sqlite_metadata_connection_config(metadata_path),
        beam_pipeline_args=['--direct_num_workers=%d' % direct_num_workers])
