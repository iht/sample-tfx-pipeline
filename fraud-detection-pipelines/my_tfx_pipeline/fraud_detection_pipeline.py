#  Copyright 2023 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import tfx.v1 as tfx
from tfx.components import StatisticsGen, SchemaGen, Transform, CsvExampleGen

import tensorflow_model_analysis as tfma

from my_tfx_pipeline import pipeline_configs


def create_pipeline(data_location: str,
                    pipeline_name: str,
                    pipeline_root: str,
                    transform_fn_file: str,
                    trainer_fn_file: str,
                    local_connection_config: str) -> tfx.dsl.Pipeline:
    # Get data from input data
    example_gen: CsvExampleGen = CsvExampleGen(input_base=data_location)

    # Data validation
    # Computes statistics over data for visualization and example validation.
    statistics_gen: StatisticsGen = None  # TODO

    # Schema inferred from stats
    schema_gen: SchemaGen = None  # TODO

    # Q: What if we don't want to infer the schema but check if the data complies with a certain schema?
    # A: We can use the ImportSchemaGen component, from a schema specified in some location (e.g. GCS)
    # schema_gen = tfx.components.ImportSchemaGen(
    #     schema_file='/some/path/schema.pbtxt')

    # Performs anomaly detection based on statistics and data schema.
    # The output contains anomalies info (data drift, skew training-test)
    example_validator = None  # TODO

    # See https://www.tensorflow.org/tfx/data_validation/get_started
    # Q: What are the thresholds used to decide if an anomaly should stop the pipeline?
    # A: Those are encoded in the schema, see an example at https://www.tensorflow.org/tfx/tutorials/tfx/penguin_tfdv
    # See all the annotations/thresholds you can set at:
    # https://github.com/tensorflow/metadata/blob/master/tensorflow_metadata/proto/v0/schema.proto

    # These are the types of anomalies that are detected:
    # https://github.com/tensorflow/metadata/blob/master/tensorflow_metadata/proto/v0/anomalies.proto

    # Feature engineering
    transform: Transform = None  # TODO

    # Training

    trainer = None  # TODO

    # Evaluate model (against baseline)
    model_resolver = tfx.dsl.Resolver(
        strategy_class=tfx.dsl.experimental.LatestBlessedModelStrategy,
        model=tfx.dsl.Channel(type=tfx.types.standard_artifacts.Model),
        model_blessing=tfx.dsl.Channel(
            type=tfx.types.standard_artifacts.ModelBlessing)).with_id(
        'latest_blessed_model_resolver')

    # Metrics to be checked
    eval_config = tfma.EvalConfig(
        model_specs=[tfma.ModelSpec(label_key='Class')],
        slicing_specs=[tfma.SlicingSpec()],
        metrics_specs=[
            tfma.MetricsSpec(per_slice_thresholds={
                'binary_accuracy':
                    tfma.PerSliceMetricThresholds(thresholds=[
                        tfma.PerSliceMetricThreshold(
                            slicing_specs=[tfma.SlicingSpec()],
                            threshold=tfma.MetricThreshold(
                                value_threshold=tfma.GenericValueThreshold(
                                    lower_bound={'value': 0.6}))
                        )]),
            })])

    evaluator = None  # TODO

    # Publish model
    pusher = tfx.components.Pusher(
        model=trainer.outputs['model'],
        model_blessing=evaluator.outputs['blessing'],
        push_destination=tfx.proto.PushDestination(
            filesystem=tfx.proto.PushDestination.Filesystem(
                base_directory=pipeline_configs.SERVING_MODEL_DIR)))

    components = [example_gen,
                  statistics_gen,
                  schema_gen,
                  example_validator,
                  transform,
                  trainer,
                  pusher,
                  model_resolver,
                  evaluator]

    pipeline = tfx.dsl.Pipeline(pipeline_name=pipeline_name,
                                pipeline_root=pipeline_root,
                                components=components,
                                metadata_connection_config=local_connection_config,
                                enable_cache=True)

    return pipeline
