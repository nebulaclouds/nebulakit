import typing

import pandas as pd
import pyspark
from pyspark.sql.dataframe import DataFrame

from nebulakit import NebulaContext
from nebulakit.models import literals
from nebulakit.models.literals import StructuredDatasetMetadata
from nebulakit.models.types import StructuredDatasetType
from nebulakit.types.structured.structured_dataset import (
    PARQUET,
    StructuredDataset,
    StructuredDatasetDecoder,
    StructuredDatasetEncoder,
    StructuredDatasetTransformerEngine,
)


class SparkDataFrameRenderer:
    """
    Render a Spark dataframe schema as an HTML table.
    """

    def to_html(self, df: DataFrame) -> str:
        assert isinstance(df, DataFrame)
        return pd.DataFrame(df.schema, columns=["StructField"]).to_html()


class SparkToParquetEncodingHandler(StructuredDatasetEncoder):
    def __init__(self):
        super().__init__(DataFrame, None, PARQUET)

    def encode(
        self,
        ctx: NebulaContext,
        structured_dataset: StructuredDataset,
        structured_dataset_type: StructuredDatasetType,
    ) -> literals.StructuredDataset:
        path = typing.cast(str, structured_dataset.uri)
        if not path:
            path = ctx.file_access.join(
                ctx.file_access.raw_output_prefix,
                ctx.file_access.get_random_string(),
            )
        df = typing.cast(DataFrame, structured_dataset.dataframe)
        ss = pyspark.sql.SparkSession.builder.getOrCreate()
        # Avoid generating SUCCESS files
        ss.conf.set("mapreduce.fileoutputcommitter.marksuccessfuljobs", "false")
        df.write.mode("overwrite").parquet(path=path)
        return literals.StructuredDataset(uri=path, metadata=StructuredDatasetMetadata(structured_dataset_type))


class ParquetToSparkDecodingHandler(StructuredDatasetDecoder):
    def __init__(self):
        super().__init__(DataFrame, None, PARQUET)

    def decode(
        self,
        ctx: NebulaContext,
        nebula_value: literals.StructuredDataset,
        current_task_metadata: StructuredDatasetMetadata,
    ) -> DataFrame:
        user_ctx = NebulaContext.current_context().user_space_params
        if current_task_metadata.structured_dataset_type and current_task_metadata.structured_dataset_type.columns:
            columns = [c.name for c in current_task_metadata.structured_dataset_type.columns]
            return user_ctx.spark_session.read.parquet(nebula_value.uri).select(*columns)
        return user_ctx.spark_session.read.parquet(nebula_value.uri)


StructuredDatasetTransformerEngine.register(SparkToParquetEncodingHandler())
StructuredDatasetTransformerEngine.register(ParquetToSparkDecodingHandler())
StructuredDatasetTransformerEngine.register_renderer(DataFrame, SparkDataFrameRenderer())
