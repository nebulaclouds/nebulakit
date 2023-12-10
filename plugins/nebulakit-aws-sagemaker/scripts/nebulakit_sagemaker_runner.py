import argparse
import logging
import os
import subprocess
import sys

NEBULA_ARG_PREFIX = "--__NEBULA"
NEBULA_ENV_VAR_PREFIX = f"{NEBULA_ARG_PREFIX}_ENV_VAR_"
NEBULA_CMD_PREFIX = f"{NEBULA_ARG_PREFIX}_CMD_"
NEBULA_ARG_SUFFIX = "__"


# This script is the "entrypoint" script for SageMaker. An environment variable must be set on the container (typically
# in the Dockerfile) of SAGEMAKER_PROGRAM=nebulakit_sagemaker_runner.py. When the container is launched in SageMaker,
# it'll run `train nebulakit_sagemaker_runner.py <hyperparameters>`, the responsibility of this script is then to decode
# the known hyperparameters (passed as command line args) to recreate the original command that will actually run the
# virtual environment and execute the intended task (e.g. `service_venv pynebula-execute --task-module ....`)

# An example for a valid command:
# python nebulakit_sagemaker_runner.py --__NEBULA_ENV_VAR_env1__ val1 --__NEBULA_ENV_VAR_env2__ val2
# --__NEBULA_CMD_0_service_venv__ __NEBULA_CMD_DUMMY_VALUE__
# --__NEBULA_CMD_1_pynebula-execute__ __NEBULA_CMD_DUMMY_VALUE__
# --__NEBULA_CMD_2_--task-module__ __NEBULA_CMD_DUMMY_VALUE__
# --__NEBULA_CMD_3_blah__ __NEBULA_CMD_DUMMY_VALUE__
# --__NEBULA_CMD_4_--task-name__ __NEBULA_CMD_DUMMY_VALUE__
# --__NEBULA_CMD_5_bloh__ __NEBULA_CMD_DUMMY_VALUE__
# --__NEBULA_CMD_6_--output-prefix__ __NEBULA_CMD_DUMMY_VALUE__
# --__NEBULA_CMD_7_s3://fake-bucket__ __NEBULA_CMD_DUMMY_VALUE__
# --__NEBULA_CMD_8_--inputs__ __NEBULA_CMD_DUMMY_VALUE__
# --__NEBULA_CMD_9_s3://fake-bucket__ __NEBULA_CMD_DUMMY_VALUE__


def parse_args(cli_args):
    parser = argparse.ArgumentParser(description="Running sagemaker task")
    args, unknowns = parser.parse_known_args(cli_args)

    # Parse the command line and env vars
    nebula_cmd = []
    env_vars = {}
    i = 0

    while i < len(unknowns):
        unknown = unknowns[i]
        logging.info(f"Processing argument {unknown}")
        if unknown.startswith(NEBULA_CMD_PREFIX) and unknown.endswith(NEBULA_ARG_SUFFIX):
            processed = unknown[len(NEBULA_CMD_PREFIX) :][: -len(NEBULA_ARG_SUFFIX)]
            # Parse the format `1_--task-module`
            parts = processed.split("_", maxsplit=1)
            nebula_cmd.append((parts[0], parts[1]))
            i += 1
        elif unknown.startswith(NEBULA_ENV_VAR_PREFIX) and unknown.endswith(NEBULA_ARG_SUFFIX):
            processed = unknown[len(NEBULA_ENV_VAR_PREFIX) :][: -len(NEBULA_ARG_SUFFIX)]
            i += 1
            if unknowns[i].startswith(NEBULA_ARG_PREFIX) is False:
                env_vars[processed] = unknowns[i]
                i += 1
        else:
            # To prevent SageMaker from ignoring our __NEBULA_CMD_*__ hyperparameters, we need to set a dummy value
            # which serves as a placeholder for each of them. The dummy value placeholder `__NEBULA_CMD_DUMMY_VALUE__`
            # falls into this branch and will be ignored
            i += 1

    return nebula_cmd, env_vars


def sort_nebula_cmd(nebula_cmd):
    # Order the cmd using the index (the first element in each tuple)
    nebula_cmd = sorted(nebula_cmd, key=lambda x: int(x[0]))
    nebula_cmd = [x[1] for x in nebula_cmd]
    return nebula_cmd


def set_env_vars(env_vars):
    for key, val in env_vars.items():
        os.environ[key] = val


def run(cli_args):
    nebula_cmd, env_vars = parse_args(cli_args)
    nebula_cmd = sort_nebula_cmd(nebula_cmd)
    set_env_vars(env_vars)

    logging.info(f"Cmd:{nebula_cmd}")
    logging.info(f"Env vars:{env_vars}")

    # Launching a subprocess with the selected entrypoint script and the rest of the arguments
    logging.info(f"Launching command: {nebula_cmd}")
    subprocess.run(nebula_cmd, stdout=sys.stdout, stderr=sys.stderr, encoding="utf-8", check=True)


if __name__ == "__main__":
    run(sys.argv)
