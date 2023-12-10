"""Test joblib file."""

import os
import typing

import joblib

import nebulakit
from nebulakit import task, workflow
from nebulakit.types.file import JoblibSerializedFile


@task
def joblib_task(obj: typing.List[int]) -> JoblibSerializedFile:
    working_dir = nebulakit.current_context().working_directory
    filename = os.path.join(working_dir, "object.joblib")
    joblib.dump(obj, filename)
    return JoblibSerializedFile(path=filename)


@workflow
def joblib_workflow(obj: typing.List[int]) -> JoblibSerializedFile:
    return joblib_task(obj=obj)
