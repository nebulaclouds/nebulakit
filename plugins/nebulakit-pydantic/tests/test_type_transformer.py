import datetime as dt
import os
import pathlib
from typing import Any, Dict, List, Optional, Type, Union

import pandas as pd
import pytest
from nebulaidl.core.types_pb2 import SimpleType
from nebulakitplugins.pydantic import BaseModelTransformer
from nebulakitplugins.pydantic.commons import PYDANTIC_SUPPORTED_NEBULA_TYPES
from pydantic import BaseModel, Extra

import nebulakit
from nebulakit.core import context_manager
from nebulakit.core.type_engine import TypeEngine
from nebulakit.types import directory
from nebulakit.types.file import file


class TrainConfig(BaseModel):
    """Config BaseModel for testing purposes."""

    batch_size: int = 32
    lr: float = 1e-3
    loss: str = "cross_entropy"

    class Config:
        extra = Extra.forbid


class Config(BaseModel):
    """Config BaseModel for testing purposes with an optional type hint."""

    model_config: Optional[Union[Dict[str, TrainConfig], TrainConfig]] = TrainConfig()


class ConfigWithDatetime(BaseModel):
    """Config BaseModel for testing purposes with datetime type hint."""

    datetime: dt.datetime = dt.datetime.now()


class NestedConfig(BaseModel):
    """Nested config BaseModel for testing purposes."""

    files: "ConfigWithNebulaFiles"
    dirs: "ConfigWithNebulaDirs"
    df: "ConfigWithPandasDataFrame"
    datetime: "ConfigWithDatetime" = ConfigWithDatetime()

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, NestedConfig) and all(
            getattr(self, attr) == getattr(__value, attr) for attr in ["files", "dirs", "df", "datetime"]
        )


class ConfigRequired(BaseModel):
    """Config BaseModel for testing purposes with required attribute."""

    model_config: Union[Dict[str, TrainConfig], TrainConfig]


class ConfigWithNebulaFiles(BaseModel):
    """Config BaseModel for testing purposes with nebulakit.files.NebulaFile type hint."""

    nebulafiles: List[file.NebulaFile]

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, ConfigWithNebulaFiles) and all(
            pathlib.Path(self_file).read_text() == pathlib.Path(other_file).read_text()
            for self_file, other_file in zip(self.nebulafiles, __value.nebulafiles)
        )


class ConfigWithNebulaDirs(BaseModel):
    """Config BaseModel for testing purposes with nebulakit.directory.NebulaDirectory type hint."""

    nebuladirs: List[directory.NebulaDirectory]

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, ConfigWithNebulaDirs) and all(
            os.listdir(self_dir) == os.listdir(other_dir)
            for self_dir, other_dir in zip(self.nebuladirs, __value.nebuladirs)
        )


class ConfigWithPandasDataFrame(BaseModel):
    """Config BaseModel for testing purposes with pandas.DataFrame type hint."""

    df: pd.DataFrame

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, ConfigWithPandasDataFrame) and self.df.equals(__value.df)


class ChildConfig(Config):
    """Child class config BaseModel for testing purposes."""

    d: List[int] = [1, 2, 3]


NestedConfig.update_forward_refs()


@pytest.mark.parametrize(
    "python_type,kwargs",
    [
        (Config, {}),
        (ConfigRequired, {"model_config": TrainConfig()}),
        (TrainConfig, {}),
        (ConfigWithNebulaFiles, {"nebulafiles": ["tests/folder/test_file1.txt", "tests/folder/test_file2.txt"]}),
        (ConfigWithNebulaDirs, {"nebuladirs": ["tests/folder/"]}),
        (ConfigWithPandasDataFrame, {"df": pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})}),
        (
            NestedConfig,
            {
                "files": {"nebulafiles": ["tests/folder/test_file1.txt", "tests/folder/test_file2.txt"]},
                "dirs": {"nebuladirs": ["tests/folder/"]},
                "df": {"df": pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})},
            },
        ),
    ],
)
def test_transform_round_trip(python_type: Type, kwargs: Dict[str, Any]):
    """Test that a (de-)serialization roundtrip results in the identical BaseModel."""

    ctx = context_manager.NebulaContextManager().current_context()

    type_transformer = BaseModelTransformer()

    python_value = python_type(**kwargs)

    literal_value = type_transformer.to_literal(
        ctx,
        python_value,
        python_type,
        type_transformer.get_literal_type(python_value),
    )

    reconstructed_value = type_transformer.to_python_value(ctx, literal_value, type(python_value))

    assert reconstructed_value == python_value


@pytest.mark.parametrize(
    "config_type,kwargs",
    [
        (Config, {"model_config": {"foo": TrainConfig(loss="mse")}}),
        (ConfigRequired, {"model_config": {"foo": TrainConfig(loss="mse")}}),
        (ConfigWithNebulaFiles, {"nebulafiles": ["tests/folder/test_file1.txt"]}),
        (ConfigWithNebulaDirs, {"nebuladirs": ["tests/folder/"]}),
        (ConfigWithPandasDataFrame, {"df": pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})}),
        (
            NestedConfig,
            {
                "files": {"nebulafiles": ["tests/folder/test_file1.txt", "tests/folder/test_file2.txt"]},
                "dirs": {"nebuladirs": ["tests/folder/"]},
                "df": {"df": pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})},
            },
        ),
    ],
)
def test_pass_to_workflow(config_type: Type, kwargs: Dict[str, Any]):
    """Test passing a BaseModel instance to a workflow works."""
    cfg = config_type(**kwargs)

    @nebulakit.task
    def train(cfg: config_type) -> config_type:
        return cfg

    @nebulakit.workflow
    def wf(cfg: config_type) -> config_type:
        return train(cfg=cfg)

    returned_cfg = wf(cfg=cfg)  # type: ignore

    assert returned_cfg == cfg
    # TODO these assertions are not valid for all types


@pytest.mark.parametrize(
    "kwargs",
    [
        {"nebulafiles": ["tests/folder/test_file1.txt", "tests/folder/test_file2.txt"]},
    ],
)
def test_nebulafiles_in_wf(kwargs: Dict[str, Any]):
    """Test passing a BaseModel instance to a workflow works."""
    cfg = ConfigWithNebulaFiles(**kwargs)

    @nebulakit.task
    def read(cfg: ConfigWithNebulaFiles) -> str:
        with open(cfg.nebulafiles[0], "r") as f:
            return f.read()

    @nebulakit.workflow
    def wf(cfg: ConfigWithNebulaFiles) -> str:
        return read(cfg=cfg)  # type: ignore

    string = wf(cfg=cfg)
    assert string in {"foo\n", "bar\n"}  # type: ignore


@pytest.mark.parametrize(
    "kwargs",
    [
        {"nebuladirs": ["tests/folder/"]},
    ],
)
def test_nebuladirs_in_wf(kwargs: Dict[str, Any]):
    """Test passing a BaseModel instance to a workflow works."""
    cfg = ConfigWithNebulaDirs(**kwargs)

    @nebulakit.task
    def listdir(cfg: ConfigWithNebulaDirs) -> List[str]:
        return os.listdir(cfg.nebuladirs[0])

    @nebulakit.workflow
    def wf(cfg: ConfigWithNebulaDirs) -> List[str]:
        return listdir(cfg=cfg)  # type: ignore

    dirs = wf(cfg=cfg)
    assert len(dirs) == 2  # type: ignore


def test_double_config_in_wf():
    """Test passing a BaseModel instance to a workflow works."""
    cfg1 = TrainConfig(batch_size=13)
    cfg2 = TrainConfig(batch_size=31)

    @nebulakit.task
    def are_different(cfg1: TrainConfig, cfg2: TrainConfig) -> bool:
        return cfg1 != cfg2

    @nebulakit.workflow
    def wf(cfg1: TrainConfig, cfg2: TrainConfig) -> bool:
        return are_different(cfg1=cfg1, cfg2=cfg2)  # type: ignore

    assert wf(cfg1=cfg1, cfg2=cfg2), wf(cfg1=cfg1, cfg2=cfg2)  # type: ignore


@pytest.mark.parametrize(
    "python_type,config_kwargs",
    [
        (Config, {}),
        (ConfigRequired, {"model_config": TrainConfig()}),
        (TrainConfig, {}),
        (ConfigWithNebulaFiles, {"nebulafiles": ["tests/folder/test_file1.txt", "tests/folder/test_file2.txt"]}),
        (ConfigWithNebulaDirs, {"nebuladirs": ["tests/folder/"]}),
        (ConfigWithPandasDataFrame, {"df": pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})}),
        (
            NestedConfig,
            {
                "files": {"nebulafiles": ["tests/folder/test_file1.txt", "tests/folder/test_file2.txt"]},
                "dirs": {"nebuladirs": ["tests/folder/"]},
                "df": {"df": pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})},
            },
        ),
    ],
)
def test_dynamic(python_type: Type[BaseModel], config_kwargs: Dict[str, Any]):
    config_instance = python_type(**config_kwargs)

    @nebulakit.task
    def train(cfg: BaseModel):
        print(cfg)

    @nebulakit.dynamic(cache=True, cache_version="0.3")
    def sub_wf(cfg: BaseModel):
        train(cfg=cfg)

    @nebulakit.workflow
    def wf():
        sub_wf(cfg=config_instance)

    wf()


def test_supported():
    assert len(PYDANTIC_SUPPORTED_NEBULA_TYPES) == 9


def test_single_df():
    ctx = context_manager.NebulaContextManager.current_context()
    lt = TypeEngine.to_literal_type(ConfigWithPandasDataFrame)
    assert lt.simple == SimpleType.STRUCT

    pyd = ConfigWithPandasDataFrame(df=pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))
    lit = TypeEngine.to_literal(ctx, pyd, ConfigWithPandasDataFrame, lt)
    assert lit.map is not None
    offloaded_keys = list(lit.map.literals["Serialized Nebula Objects"].map.literals.keys())
    assert len(offloaded_keys) == 1
    assert (
        lit.map.literals["Serialized Nebula Objects"].map.literals[offloaded_keys[0]].scalar.structured_dataset
        is not None
    )
