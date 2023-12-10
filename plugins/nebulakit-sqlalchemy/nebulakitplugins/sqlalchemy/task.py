import typing
from dataclasses import dataclass

import pandas as pd
from pandas.io.sql import pandasSQL_builder
from sqlalchemy import create_engine, text  # type: ignore

from nebulakit import current_context, kwtypes
from nebulakit.configuration import SerializationSettings
from nebulakit.configuration.default_images import DefaultImages, PythonVersion
from nebulakit.core.base_sql_task import SQLTask
from nebulakit.core.python_customized_container_task import PythonCustomizedContainerTask
from nebulakit.core.shim_task import ShimTaskExecutor
from nebulakit.loggers import logger
from nebulakit.models import task as task_models
from nebulakit.models.security import Secret
from nebulakit.types.schema import NebulaSchema


class SQLAlchemyDefaultImages(DefaultImages):
    """Default images for the sqlalchemy nebulakit plugin."""

    _DEFAULT_IMAGE_PREFIXES = {
        PythonVersion.PYTHON_3_8: "cr.nebula.org/nebulaclouds/nebulakit:py3.8-sqlalchemy-",
        PythonVersion.PYTHON_3_9: "cr.nebula.org/nebulaclouds/nebulakit:py3.9-sqlalchemy-",
        PythonVersion.PYTHON_3_10: "cr.nebula.org/nebulaclouds/nebulakit:py3.10-sqlalchemy-",
        PythonVersion.PYTHON_3_11: "cr.nebula.org/nebulaclouds/nebulakit:py3.11-sqlalchemy-",
    }


@dataclass
class SQLAlchemyConfig(object):
    """
    Use this configuration to configure task. String should be standard
    sqlalchemy connector format
    (https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls).
    Database can be found:
    - within the container
    - or from a publicly accessible source

    Args:
        uri: default sqlalchemy connector
        connect_args: sqlalchemy kwarg overrides -- ex: host
        secret_connect_args: nebula secrets loaded into sqlalchemy connect args
            -- ex: {"password": nebulakit.models.security.Secret(name=SECRET_NAME, group=SECRET_GROUP)}
    """

    uri: str
    connect_args: typing.Optional[typing.Dict[str, typing.Any]] = None
    secret_connect_args: typing.Optional[typing.Dict[str, Secret]] = None

    @staticmethod
    def _secret_to_dict(secret: Secret) -> typing.Dict[str, typing.Optional[str]]:
        return {
            "group": secret.group,
            "key": secret.key,
            "group_version": secret.group_version,
            "mount_requirement": secret.mount_requirement.value,
        }

    def secret_connect_args_to_dicts(self) -> typing.Optional[typing.Dict[str, typing.Dict[str, typing.Optional[str]]]]:
        if self.secret_connect_args is None:
            return None

        secret_connect_args_dicts = {}
        for key, secret in self.secret_connect_args.items():
            secret_connect_args_dicts[key] = self._secret_to_dict(secret)

        return secret_connect_args_dicts


class SQLAlchemyTask(PythonCustomizedContainerTask[SQLAlchemyConfig], SQLTask[SQLAlchemyConfig]):
    """
    Makes it possible to run client side SQLAlchemy queries that optionally return a NebulaSchema object
    """

    # TODO: How should we use pre-built containers for running portable tasks like this? Should this always be a referenced task type?

    _SQLALCHEMY_TASK_TYPE = "sqlalchemy"

    def __init__(
        self,
        name: str,
        query_template: str,
        task_config: SQLAlchemyConfig,
        inputs: typing.Optional[typing.Dict[str, typing.Type]] = None,
        output_schema_type: typing.Optional[typing.Type[NebulaSchema]] = NebulaSchema,
        container_image: str = SQLAlchemyDefaultImages.default_image(),
        **kwargs,
    ):
        if output_schema_type:
            outputs = kwtypes(results=output_schema_type)
        else:
            outputs = None

        super().__init__(
            name=name,
            task_config=task_config,
            executor_type=SQLAlchemyTaskExecutor,
            task_type=self._SQLALCHEMY_TASK_TYPE,
            query_template=query_template,
            container_image=container_image,
            inputs=inputs,
            outputs=outputs,
            **kwargs,
        )

    @property
    def output_columns(self) -> typing.Optional[typing.List[str]]:
        c = self.python_interface.outputs["results"].column_names()
        return c if c else None

    def get_custom(self, settings: SerializationSettings) -> typing.Dict[str, typing.Any]:
        return {
            "query_template": self.query_template,
            "uri": self.task_config.uri,
            "connect_args": self.task_config.connect_args or {},
            "secret_connect_args": self.task_config.secret_connect_args_to_dicts(),
        }


class SQLAlchemyTaskExecutor(ShimTaskExecutor[SQLAlchemyTask]):
    def execute_from_model(self, tt: task_models.TaskTemplate, **kwargs) -> typing.Any:
        if tt.custom["secret_connect_args"] is not None:
            for key, secret_dict in tt.custom["secret_connect_args"].items():
                value = current_context().secrets.get(group=secret_dict["group"], key=secret_dict["key"])
                tt.custom["connect_args"][key] = value

        engine = create_engine(tt.custom["uri"], connect_args=tt.custom["connect_args"], echo=False)
        logger.info(f"Connecting to db {tt.custom['uri']}")

        interpolated_query = SQLAlchemyTask.interpolate_query(tt.custom["query_template"], **kwargs)
        logger.info(f"Interpolated query {interpolated_query}")
        with engine.begin() as connection:
            df = None
            if tt.interface.outputs:
                df = pd.read_sql_query(text(interpolated_query), connection)
            else:
                pandasSQL_builder(connection).execute(text(interpolated_query))
        return df
