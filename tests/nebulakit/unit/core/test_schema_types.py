from datetime import datetime, timedelta

import pandas as pd
import pytest

from nebulakit import kwtypes
from nebulakit.core import context_manager
from nebulakit.core.context_manager import ExecutionState, NebulaContextManager
from nebulakit.core.type_engine import TypeEngine
from nebulakit.types.schema import NebulaSchema, SchemaFormat
from nebulakit.types.schema.types import NebulaSchemaTransformer
from nebulakit.types.schema.types_pandas import PandasDataFrameTransformer


def test_typed_schema():
    s = NebulaSchema[kwtypes(x=int, y=float)]
    assert s.format() == SchemaFormat.PARQUET
    assert s.columns() == {"x": int, "y": float}


def test_assert_type():
    ctx = context_manager.NebulaContextManager.current_context()
    with context_manager.NebulaContextManager.with_context(
        ctx.with_execution_state(ctx.new_execution_state().with_params(mode=ExecutionState.Mode.TASK_EXECUTION))
    ) as ctx:
        schema = NebulaSchema[kwtypes(x=int, y=float)]
        fst = NebulaSchemaTransformer()
        lt = fst.get_literal_type(schema)
        with pytest.raises(ValueError, match="DataFrames of type <class 'int'> are not supported currently"):
            TypeEngine.to_literal(ctx, 3, schema, lt)


def test_schema_back_and_forth():
    orig = NebulaSchema[kwtypes(TrackId=int, Name=str)]
    lt = TypeEngine.to_literal_type(orig)
    pt = TypeEngine.guess_python_type(lt)
    lt2 = TypeEngine.to_literal_type(pt)
    assert lt == lt2


def test_remaining_prims():
    orig = NebulaSchema[kwtypes(my_dt=datetime, my_td=timedelta, my_b=bool)]
    lt = TypeEngine.to_literal_type(orig)
    pt = TypeEngine.guess_python_type(lt)
    lt2 = TypeEngine.to_literal_type(pt)
    assert lt == lt2


def test_bad_conversion():
    orig = NebulaSchema[kwtypes(my_custom=bool)]
    lt = TypeEngine.to_literal_type(orig)
    # Make a not real column type
    lt.schema.columns[0]._type = 15
    with pytest.raises(ValueError):
        TypeEngine.guess_python_type(lt)


def test_to_html():
    df = pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [20, 22]})
    tf = PandasDataFrameTransformer()
    output = tf.to_html(NebulaContextManager.current_context(), df, pd.DataFrame)
    assert df.describe().to_html() == output
