import datetime
import os
import typing
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Type, Union

import great_expectations as ge
from dataclasses_json import DataClassJsonMixin
from great_expectations.checkpoint import SimpleCheckpoint
from great_expectations.core.run_identifier import RunIdentifier
from great_expectations.core.util import convert_to_json_serializable
from great_expectations.exceptions import ValidationError

from nebulakit import NebulaContext
from nebulakit.extend import TypeEngine, TypeTransformer
from nebulakit.loggers import logger
from nebulakit.models import types as _type_models
from nebulakit.models.literals import Literal, Primitive, Scalar
from nebulakit.models.types import LiteralType
from nebulakit.types.file.file import NebulaFile, NebulaFilePathTransformer
from nebulakit.types.schema.types import NebulaSchema, NebulaSchemaTransformer

from .task import BatchRequestConfig


@dataclass
class GreatExpectationsNebulaConfig(DataClassJsonMixin):
    """
    Use this configuration to configure GreatExpectations Plugin.

    Args:
        datasource_name: tell where your data lives and how to get it
        expectation_suite_name: suite which consists of the data expectations
        data_connector_name: connector to identify data batches
        data_asset_name: name of the data asset (to be used for RuntimeBatchRequest)
        local_file_path: dataset file path useful for NebulaFile and NebulaSchema
        checkpoint_params: optional SimpleCheckpoint parameters
        batch_request_config: batchrequest config
        context_root_dir: directory in which GreatExpectations' configuration resides
    """

    datasource_name: str
    expectation_suite_name: str
    data_connector_name: str
    data_asset_name: Optional[str] = None
    """
    local_file_path is a must in two scenrios:
    * When using NebulaSchema
    * When using NebulaFile for remote paths
    This is because base directory which has the dataset file 'must' be given in GreatExpectations' config file
    """
    local_file_path: Optional[str] = None
    checkpoint_params: Optional[Dict[str, Union[str, List[str]]]] = None
    batch_request_config: Optional[BatchRequestConfig] = None
    context_root_dir: str = "./great_expectations"


class GreatExpectationsType(object):
    """
    Use this class to send the GreatExpectationsNebulaConfig.

    Args:
        config: GreatExpectations Plugin configuration

    TODO: Connect Data Docs to Nebula Console.
    """

    @classmethod
    def config(cls) -> Tuple[Type, GreatExpectationsNebulaConfig]:
        return (
            str,
            GreatExpectationsNebulaConfig(datasource_name="", data_connector_name="", expectation_suite_name=""),
        )

    def __class_getitem__(cls, config: Tuple[Type, GreatExpectationsNebulaConfig]) -> Any:
        if not (isinstance(config, tuple) or len(config) != 2):
            raise AssertionError("GreatExpectationsType must have both datatype and GreatExpectationsNebulaConfig")

        class _GreatExpectationsTypeClass(GreatExpectationsType):
            __origin__ = GreatExpectationsType

            @classmethod
            def config(cls) -> Tuple[Type, GreatExpectationsNebulaConfig]:
                return config

        return _GreatExpectationsTypeClass


class GreatExpectationsTypeTransformer(TypeTransformer[GreatExpectationsType]):
    def __init__(self):
        super().__init__(name="GreatExpectations Transformer", t=GreatExpectationsType)

    @staticmethod
    def get_config(t: Type[GreatExpectationsType]) -> Tuple[Type, GreatExpectationsNebulaConfig]:
        return t.config()

    def get_literal_type(self, t: Type[GreatExpectationsType]) -> LiteralType:
        datatype = GreatExpectationsTypeTransformer.get_config(t)[0]

        if issubclass(datatype, str):
            return LiteralType(simple=_type_models.SimpleType.STRING, metadata={})
        elif issubclass(datatype, NebulaFile):
            return NebulaFilePathTransformer().get_literal_type(datatype)
        elif issubclass(datatype, NebulaSchema):
            return NebulaSchemaTransformer().get_literal_type(datatype)
        else:
            raise TypeError(f"{datatype} is not a supported type")

    def to_literal(
        self,
        ctx: NebulaContext,
        python_val: Union[NebulaFile, NebulaSchema, str],
        python_type: Type[GreatExpectationsType],
        expected: LiteralType,
    ) -> Literal:
        datatype = GreatExpectationsTypeTransformer.get_config(python_type)[0]

        if issubclass(datatype, NebulaSchema):
            return NebulaSchemaTransformer().to_literal(ctx, python_val, datatype, expected)
        elif issubclass(datatype, NebulaFile):
            return NebulaFilePathTransformer().to_literal(ctx, python_val, datatype, expected)
        elif issubclass(datatype, str):
            return Literal(scalar=Scalar(primitive=Primitive(string_value=python_val)))
        else:
            raise TypeError(f"{datatype} is not a supported type")

    def _nebula_schema(
        self,
        is_runtime: bool,
        ctx: NebulaContext,
        ge_conf: GreatExpectationsNebulaConfig,
        lv: Literal,
        expected_python_type: Type[NebulaSchema],
    ) -> (NebulaSchema, str):
        temp_dataset = ""

        # if data batch is to be generated, skip copying the parquet file
        if not is_runtime:
            if not ge_conf.local_file_path:
                raise ValueError("local_file_path is missing!")

            # copy parquet file to user-given directory
            if lv.scalar.structured_dataset:
                ctx.file_access.get_data(lv.scalar.structured_dataset.uri, ge_conf.local_file_path, is_multipart=True)
            else:
                ctx.file_access.get_data(lv.scalar.schema.uri, ge_conf.local_file_path, is_multipart=True)

            temp_dataset = os.path.basename(ge_conf.local_file_path)

        return NebulaSchemaTransformer().to_python_value(ctx, lv, expected_python_type), temp_dataset

    def _nebula_file(
        self,
        ctx: NebulaContext,
        ge_conf: GreatExpectationsNebulaConfig,
        lv: Literal,
        expected_python_type: Type[NebulaFile],
    ) -> (NebulaFile, str):
        if not ge_conf.local_file_path:
            raise ValueError("local_file_path is missing!")

        uri = lv.scalar.blob.uri

        if os.path.isdir(ge_conf.local_file_path):
            local_path = os.path.join(ge_conf.local_file_path, os.path.basename(uri))
        else:
            local_path = ge_conf.local_file_path

        # download the file into local_file_path
        ctx.file_access.get_data(
            remote_path=uri,
            local_path=local_path,
        )

        return NebulaFilePathTransformer().to_python_value(ctx, lv, expected_python_type), os.path.basename(uri)

    def to_python_value(
        self,
        ctx: NebulaContext,
        lv: Literal,
        expected_python_type: Type[GreatExpectationsType],
    ) -> GreatExpectationsType:
        if not (
            lv
            and lv.scalar
            and (
                (lv.scalar.primitive and lv.scalar.primitive.string_value)
                or lv.scalar.schema
                or lv.scalar.blob
                or lv.scalar.structured_dataset
            )
        ):
            raise AssertionError("Can only validate a literal string/NebulaFile/NebulaSchema value")

        # fetch the configuration
        type_conf = GreatExpectationsTypeTransformer.get_config(expected_python_type)
        conf_dict = type_conf[1].to_dict()  # type: ignore

        ge_conf = GreatExpectationsNebulaConfig(**conf_dict)

        # fetch the data context
        context = ge.data_context.DataContext(ge_conf.context_root_dir)  # type: ignore

        # determine the type of data connector
        selected_datasource = list(filter(lambda x: x["name"] == ge_conf.datasource_name, context.list_datasources()))

        if not selected_datasource:
            raise ValueError("Datasource doesn't exist!")

        data_connector_class_lookup = {
            data_connector_name: data_connector_class["class_name"]
            for data_connector_name, data_connector_class in selected_datasource[0]["data_connectors"].items()
        }

        specified_data_connector_class = data_connector_class_lookup[ge_conf.data_connector_name]

        is_runtime = False
        if specified_data_connector_class == "RuntimeDataConnector":
            is_runtime = True
            if not ge_conf.data_asset_name:
                raise ValueError("data_asset_name has to be given in a RuntimeBatchRequest")

        # file path for NebulaSchema and NebulaFile
        temp_dataset = ""

        # return value
        return_dataset = ""

        # NebulaSchema
        if lv.scalar.schema or lv.scalar.structured_dataset:
            return_dataset, temp_dataset = self._nebula_schema(
                is_runtime=is_runtime, ctx=ctx, ge_conf=ge_conf, lv=lv, expected_python_type=type_conf[0]
            )

        # NebulaFile
        if lv.scalar.blob:
            return_dataset, temp_dataset = self._nebula_file(
                ctx=ctx, ge_conf=ge_conf, lv=lv, expected_python_type=type_conf[0]
            )

        if lv.scalar.primitive:
            dataset = return_dataset = lv.scalar.primitive.string_value
        else:
            dataset = temp_dataset

        batch_request_conf = ge_conf.batch_request_config

        # minimalistic batch request
        final_batch_request = {
            "data_asset_name": ge_conf.data_asset_name if is_runtime else dataset,
            "datasource_name": ge_conf.datasource_name,
            "data_connector_name": ge_conf.data_connector_name,
        }

        # Great Expectations' RuntimeBatchRequest
        if batch_request_conf and (batch_request_conf["runtime_parameters"] or is_runtime):
            final_batch_request.update(
                {
                    "runtime_parameters": batch_request_conf["runtime_parameters"]
                    if batch_request_conf["runtime_parameters"]
                    else {},
                    "batch_identifiers": batch_request_conf["batch_identifiers"],
                    "batch_spec_passthrough": batch_request_conf["batch_spec_passthrough"],
                }
            )

            if is_runtime and lv.scalar.primitive:
                final_batch_request["runtime_parameters"]["query"] = dataset
            elif is_runtime and (lv.scalar.schema or lv.scalar.structured_dataset):
                final_batch_request["runtime_parameters"]["batch_data"] = return_dataset.open().all()
            else:
                raise AssertionError("Can only use runtime_parameters for query(str)/schema data")

        # Great Expectations' BatchRequest
        elif batch_request_conf:
            final_batch_request.update(
                {
                    "data_connector_query": batch_request_conf["data_connector_query"],
                    "batch_spec_passthrough": batch_request_conf["batch_spec_passthrough"],
                }
            )

        if ge_conf.checkpoint_params:
            checkpoint = SimpleCheckpoint(
                f"_tmp_checkpoint_{ge_conf.expectation_suite_name}",
                context,
                **ge_conf.checkpoint_params,
            )
        else:
            checkpoint = SimpleCheckpoint(f"_tmp_checkpoint_{ge_conf.expectation_suite_name}", context)

        # identify every run uniquely
        run_id = RunIdentifier(
            **{
                "run_name": ge_conf.datasource_name + "_run",
                "run_time": datetime.datetime.utcnow(),
            }
        )

        checkpoint_result = checkpoint.run(
            run_id=run_id,
            validations=[
                {
                    "batch_request": final_batch_request,
                    "expectation_suite_name": ge_conf.expectation_suite_name,
                }
            ],
        )
        final_result = convert_to_json_serializable(checkpoint_result.list_validation_results())[0]

        result_string = ""
        if final_result["success"] is False:
            for every_result in final_result["results"]:
                if every_result["success"] is False:
                    result_string += (
                        every_result["expectation_config"]["kwargs"]["column"]
                        + " -> "
                        + every_result["expectation_config"]["expectation_type"]
                        + "\n"
                    )

            # raise a Great Expectations' exception
            raise ValidationError("Validation failed!\nCOLUMN\t\tFAILED EXPECTATION\n" + result_string)

        logger.info("Validation succeeded!")

        return typing.cast(GreatExpectationsType, return_dataset)


TypeEngine.register(GreatExpectationsTypeTransformer())
