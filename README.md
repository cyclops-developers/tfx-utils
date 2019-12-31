# Laguro tfx

Laguro TFX utils


# Description

Utilities to help writing TFX pipelines


# Example

First, create a pipeline

```
pipeline = create_classification_pipeline(
                    pipeline_name=runner['pipeline_name'],
                    pipeline_root=runner['pipeline_root'],
                    data_root=runner['data_root'],
                    schema_path=runner['schema_path'],
                    serving_model_dir=runner['serving_model_dir'],
                    metadata_path=runner['metadata_path'],
                    direct_num_workers=0))
```

Then it needs to run through a supported platform:

- Kubeflow
- Airflow
- Beam

For instance, for airflow: 

```
config = AirflowPipelineConfig(**config)
DAG = AirflowDagRunner(config).run(pipeline)
```



