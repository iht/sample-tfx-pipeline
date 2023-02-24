# ML Ops with TFX

## Setup

For this project, you will need Python 3.7, 3.8 or 3.9, with a virtualenv with 
the dependencies included in the file `requirements.txt`.

Find instructions below to install the dependencies:

Please don't use Python < 3.7 (e.g. 3.6) or Python > 3.9 (e.g. 3.10), they will 
not work with TFX. For more details, please check:

* https://www.tensorflow.org/tfx
* https://github.com/tensorflow/tfx

At the moment of writing this, the Cloud Shell has Python 3.9. You can check your 
Python version by running the following command:

```shell
python --version
```

Once you have made sure you have the correct Python version, create a virtualenv: 

```shell
python -m venv tfxenv
```

Activate it:

```shell
source ./tfxenv/bin/activate
```

And install the dependencies in the file `requirements.txt`, by running:

```shell
pip install -r requirements.txt
```

## Running the pipeline

Edit the scripts in the directory `scripts` just in case you want to adapt any of
the default options.

The `playground` branch of this repository contains incomplete code that you need to
finish, as an exercise to learn the ropes of TFX pipelines.

To run the pipeline, run this script:

```shell
./scripts/launch_local.sh
```