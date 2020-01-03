Laguro TFX utils v0.0.1
=======================

Description
--------------
Utilities to help writing TFX pipelines

Config
------
All configuration should be stored in a project specific folder.


Example
-------

First, create a pipeline::

    with open(config_file, 'r') as fp:
        config = yaml.load(fp)

    runner = config['runner']
    pipeline = create_classification_pipeline(
                        pipeline_name=runner['pipeline_name'],
                        pipeline_root=runner['pipeline_root'],
                        data_root=runner['data_root'],
                        schema_path=runner['schema_path'],
                        serving_model_dir=runner['serving_model_dir'],
                        metadata_path=runner['metadata_path'],
                        direct_num_workers=0))

Then it needs to run through a supported platform:

- Kubeflow
- Airflow
- Beam

For instance, for airflow::

    airflow_pipeline_config = AirflowPipelineConfig(config['airflow'])
    dag_runner = AirflowDagRunner(airflow_pipeline_config)
    DAG = dag_runner.run(pipeline)

It's important to notice airflow config expects objects instead of
strings, e.g, dates. So that, all date-specific fields in the config file
should be converted to :code:`python datetime`.