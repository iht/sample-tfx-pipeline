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

import argparse
import logging
import os.path

import tfx.v1 as tfx

from my_tfx_pipeline import fraud_detection_pipeline
from my_tfx_pipeline import pipeline_configs
from my_tfx_pipeline import pipeline_run


def main(data_location: str,
         pipeline_name: str,
         pipeline_root: str,
         transform_fn_file: str,
         trainer_fn_file: str):
    pipeline_definition = os.path.join("/tmp", pipeline_name + "_pipeline.json")
    runner = tfx.orchestration.experimental.KubeflowV2DagRunner(
        config=tfx.orchestration.experimental.KubeflowV2DagRunnerConfig(),
        output_filename=pipeline_definition)

    metadata_connection = tfx.orchestration.metadata.sqlite_metadata_connection_config(pipeline_configs.METADATA_PATH)

    pipeline: tfx.dsl.Pipeline = fraud_detection_pipeline.create_pipeline(
        data_location=data_location,
        pipeline_name=pipeline_name,
        pipeline_root=pipeline_root,
        transform_fn_file=transform_fn_file,
        trainer_fn_file=trainer_fn_file,
        local_connection_config=metadata_connection)

    runner.run(pipeline)  # Creates pipeline definition

    logging.getLogger().setLevel(logging.INFO)

    pipeline_run.run_locally(pipeline)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--data-location", required=True)

    parser.add_argument("--pipeline-root", required=True)
    parser.add_argument("--pipeline-name", required=True)

    parser.add_argument("--transform-fn-path", required=True)
    parser.add_argument("--trainer-fn-path", required=True)

    args = parser.parse_args()

    main(data_location=args.data_location,
         pipeline_name=args.pipeline_name,
         pipeline_root=args.pipeline_root,
         transform_fn_file=args.transform_fn_path,
         trainer_fn_file=args.trainer_fn_path)
