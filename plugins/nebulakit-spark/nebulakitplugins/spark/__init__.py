"""
.. currentmodule:: nebulakitplugins.spark

This package contains things that are useful when extending Nebulakit.

.. autosummary::
   :template: custom.rst
   :toctree: generated/

   new_spark_session
   ParquetToSparkDecodingHandler
   Spark
   SparkDataFrameSchemaReader
   SparkDataFrameSchemaWriter
   SparkDataFrameTransformer  # noqa
"""

from nebulakit.configuration import internal as _internal

from .agent import DatabricksAgent
from .pyspark_transformers import PySparkPipelineModelTransformer
from .schema import SparkDataFrameSchemaReader, SparkDataFrameSchemaWriter, SparkDataFrameTransformer  # noqa
from .sd_transformers import ParquetToSparkDecodingHandler, SparkToParquetEncodingHandler
from .task import Databricks, Spark, new_spark_session  # noqa
