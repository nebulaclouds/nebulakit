import os

import pip
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

PACKAGE_NAME = "nebulakitplugins-parent"

__version__ = "0.0.0+develop"

# Please maintain an alphabetical order in the following list
SOURCES = {
    "nebulakitplugins-athena": "nebulakit-aws-athena",
    "nebulakitplugins-awsbatch": "nebulakit-aws-batch",
    "nebulakitplugins-awssagemaker": "nebulakit-aws-sagemaker",
    "nebulakitplugins-bigquery": "nebulakit-bigquery",
    "nebulakitplugins-dask": "nebulakit-dask",
    "nebulakitplugins-dbt": "nebulakit-dbt",
    "nebulakitplugins-deck-standard": "nebulakit-deck-standard",
    "nebulakitplugins-dolt": "nebulakit-dolt",
    "nebulakitplugins-duckdb": "nebulakit-duckdb",
    "nebulakitplugins-data-fsspec": "nebulakit-data-fsspec",
    "nebulakitplugins-envd": "nebulakit-envd",
    "nebulakitplugins-great_expectations": "nebulakit-greatexpectations",
    "nebulakitplugins-hive": "nebulakit-hive",
    "nebulakitplugins-huggingface": "nebulakit-huggingface",
    "nebulakitplugins-pod": "nebulakit-k8s-pod",
    "nebulakitplugins-kfmpi": "nebulakit-kf-mpi",
    "nebulakitplugins-kfpytorch": "nebulakit-kf-pytorch",
    "nebulakitplugins-kftensorflow": "nebulakit-kf-tensorflow",
    "nebulakitplugins-mlflow": "nebulakit-mlflow",
    "nebulakitplugins-modin": "nebulakit-modin",
    "nebulakitplugins-onnxscikitlearn": "nebulakit-onnx-scikitlearn",
    "nebulakitplugins-onnxtensorflow": "nebulakit-onnx-tensorflow",
    "nebulakitplugins-onnxpytorch": "nebulakit-onnx-pytorch",
    "nebulakitplugins-pandera": "nebulakit-pandera",
    "nebulakitplugins-papermill": "nebulakit-papermill",
    "nebulakitplugins-polars": "nebulakit-polars",
    "nebulakitplugins-ray": "nebulakit-ray",
    "nebulakitplugins-snowflake": "nebulakit-snowflake",
    "nebulakitplugins-spark": "nebulakit-spark",
    "nebulakitplugins-sqlalchemy": "nebulakit-sqlalchemy",
    "nebulakitplugins-vaex": "nebulakit-vaex",
    "nebulakitplugins-whylogs": "nebulakit-whylogs",
    "nebulakitplugins-flyin": "nebulakit-flyin",
}


def install_all_plugins(sources, develop=False):
    """
    Use pip to install all plugins
    """
    print("Installing all Nebula plugins in {} mode".format("development" if develop else "normal"))
    wd = os.getcwd()
    for k, v in sources.items():
        try:
            os.chdir(os.path.join(wd, v))
            if develop:
                pip.main(["install", "-e", "."])
            else:
                pip.main(["install", "."])
        except Exception as e:
            print("Oops, something went wrong installing", k)
            print(e)
        finally:
            os.chdir(wd)


class DevelopCmd(develop):
    """Add custom steps for the develop command"""

    def run(self):
        install_all_plugins(SOURCES, develop=True)
        develop.run(self)


class InstallCmd(install):
    """Add custom steps for the install command"""

    def run(self):
        install_all_plugins(SOURCES, develop=False)
        install.run(self)


setup(
    name=PACKAGE_NAME,
    version=__version__,
    author="nebulaclouds",
    author_email="admin@nebula.org",
    description="This is a microlib package to help install all the plugins",
    license="apache2",
    classifiers=["Private :: Do Not Upload to pypi server"],
    install_requires=[],
    cmdclass={"install": InstallCmd, "develop": DevelopCmd},
)
