# Nebulakit Python Plugins

All the Nebulakit plugins maintained by the core team are added here. It is not necessary to add plugins here, but this is a good starting place.

## Currently Available Plugins 🔌

| Plugin                       | Installation                                              | Description                                                                                                                | Version                                                                                                                                                      | Type          |
|------------------------------|-----------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|
| AWS Sagemaker Training       | ```bash pip install nebulakitplugins-awssagemaker ```      | Installs SDK to author Sagemaker built-in and custom training jobs in python                                               | [![PyPI version fury.io](https://badge.fury.io/py/nebulakitplugins-awssagemaker.svg)](https://pypi.python.org/pypi/nebulakitplugins-awssagemaker/)             | Backend       |
| dask                         | ```bash pip install nebulakitplugins-dask ```              | Installs SDK to author dask jobs that can be executed natively on Kubernetes using the Nebula backend plugin                | [![PyPI version fury.io](https://badge.fury.io/py/nebulakitplugins-awssagemaker.svg)](https://pypi.python.org/pypi/nebulakitplugins-dask/)             | Backend       |
| Hive Queries                 | ```bash pip install nebulakitplugins-hive ```              | Installs SDK to author Hive Queries that can be executed on a configured hive backend using Nebula backend plugin           | [![PyPI version fury.io](https://badge.fury.io/py/nebulakitplugins-hive.svg)](https://pypi.python.org/pypi/nebulakitplugins-hive/)                             | Backend       |
| K8s distributed PyTorch Jobs | ```bash pip install nebulakitplugins-kfpytorch ```         | Installs SDK to author Distributed pyTorch Jobs in python using Kubeflow PyTorch Operator                                  | [![PyPI version fury.io](https://badge.fury.io/py/nebulakitplugins-kfpytorch.svg)](https://pypi.python.org/pypi/nebulakitplugins-kfpytorch/)                   | Backend       |
| K8s native tensorflow Jobs   | ```bash pip install nebulakitplugins-kftensorflow ```      | Installs SDK to author Distributed tensorflow Jobs in python using Kubeflow Tensorflow Operator                            | [![PyPI version fury.io](https://badge.fury.io/py/nebulakitplugins-kftensorflow.svg)](https://pypi.python.org/pypi/nebulakitplugins-kftensorflow/)             | Backend       |
| K8s native MPI Jobs          | ```bash pip install nebulakitplugins-kfmpi ```             | Installs SDK to author Distributed MPI Jobs in python using Kubeflow MPI Operator                                          | [![PyPI version fury.io](https://badge.fury.io/py/nebulakitplugins-kfmpi.svg)](https://pypi.python.org/pypi/nebulakitplugins-kfmpi/)                           | Backend       |
| Papermill based Tasks        | ```bash pip install nebulakitplugins-papermill ```         | Execute entire notebooks as Nebula Tasks and pass inputs and outputs between them and python tasks                          | [![PyPI version fury.io](https://badge.fury.io/py/nebulakitplugins-papermill.svg)](https://pypi.python.org/pypi/nebulakitplugins-papermill/)                   | Nebulakit-only |
| Pod Tasks                    | ```bash pip install nebulakitplugins-pod ```               | Installs SDK to author Pods in python. These pods can have multiple containers, use volumes and have non exiting side-cars | [![PyPI version fury.io](https://badge.fury.io/py/nebulakitplugins-pod.svg)](https://pypi.python.org/pypi/nebulakitplugins-pod/)                               | Nebulakit-only |
| spark                        | ```bash pip install nebulakitplugins-spark ```             | Installs SDK to author Spark jobs that can be executed natively on Kubernetes with a supported backend Nebula plugin        | [![PyPI version fury.io](https://badge.fury.io/py/nebulakitplugins-spark.svg)](https://pypi.python.org/pypi/nebulakitplugins-spark/)                           | Backend       |
| AWS Athena Queries           | ```bash pip install nebulakitplugins-athena ```            | Installs SDK to author queries executed on AWS Athena                                                                      | [![PyPI version fury.io](https://badge.fury.io/py/nebulakitplugins-athena.svg)](https://pypi.python.org/pypi/nebulakitplugins-athena/)                         | Backend       |
| DOLT                         | ```bash pip install nebulakitplugins-dolt ```              | Read & write dolt data sets and use dolt tables as native types                                                            | [![PyPI version fury.io](https://badge.fury.io/py/nebulakitplugins-dolt.svg)](https://pypi.python.org/pypi/nebulakitplugins-dolt/)                             | Nebulakit-only |
| Pandera                      | ```bash pip install nebulakitplugins-pandera ```           | Use Pandera schemas as native Nebula types, which enable data quality checks.                                               | [![PyPI version fury.io](https://badge.fury.io/py/nebulakitplugins-pandera.svg)](https://pypi.python.org/pypi/nebulakitplugins-pandera/)                       | Nebulakit-only |
| SQLAlchemy                   | ```bash pip install nebulakitplugins-sqlalchemy ```        | Write queries for any database that supports SQLAlchemy                                                                    | [![PyPI version fury.io](https://badge.fury.io/py/nebulakitplugins-sqlalchemy.svg)](https://pypi.python.org/pypi/nebulakitplugins-sqlalchemy/)                 | Nebulakit-only |
| Great Expectations           | ```bash pip install nebulakitplugins-great-expectations``` | Enforce data quality for various data types within Nebula                                                                   | [![PyPI version fury.io](https://badge.fury.io/py/nebulakitplugins-great-expectations.svg)](https://pypi.python.org/pypi/nebulakitplugins-great-expectations/) | Nebulakit-only |
| Snowflake                    | ```bash pip install nebulakitplugins-snowflake```          | Use Snowflake as a 'data warehouse-as-a-service' within Nebula                                                              | [![PyPI version fury.io](https://badge.fury.io/py/nebulakitplugins-snowflake.svg)](https://pypi.python.org/pypi/nebulakitplugins-snowflake/)                   | Backend       |
| dbt                          | ```bash pip install nebulakitplugins-dbt```                | Run dbt within Nebula                                                                                                       | [![PyPI version fury.io](https://badge.fury.io/py/nebulakitplugins-dbt.svg)](https://pypi.python.org/pypi/nebulakitplugins-dbt/)                               | Nebulakit-only |
| Huggingface                  | ```bash pip install nebulakitplugins-huggingface```        | Read & write Hugginface Datasets as Nebula StructuredDatasets                                                               | [![PyPI version fury.io](https://badge.fury.io/py/nebulakitplugins-huggingface.svg)](https://pypi.python.org/pypi/nebulakitplugins-huggingface/)               | Nebulakit-only |
| DuckDB                  | ```bash pip install nebulakitplugins-duckdb```        | Run analytical workloads with ease using DuckDB.
| [![PyPI version fury.io](https://badge.fury.io/py/nebulakitplugins-duckdb.svg)](https://pypi.python.org/pypi/nebulakitplugins-duckdb/)               | Nebulakit-only |

## Have a Plugin Idea? 💡
Please [file an issue](https://github.com/nebulaclouds/nebula/issues/new?assignees=&labels=untriaged%2Cplugins&template=backend-plugin-request.md&title=%5BPlugin%5D).

## Development 💻
Nebulakit plugins are structured as micro-libs and can be authored in an independent repository.

> Refer to the [Python microlibs](https://medium.com/@jherreras/python-microlibs-5be9461ad979) blog to understand the idea of microlibs.

The plugins maintained by the core team can be found in this repository and provide a simple way of discovery.

## Unit tests 🧪
Plugins should have their own unit tests.

## Guidelines 📜
Some guidelines to help you write the Nebulakit plugins better.

1. The folder name has to be `nebulakit-*`, e.g., `nebulakit-hive`. In case you want to group for a specific service, then use `nebulakit-aws-athena`.
2. Nebulakit plugins use a concept called [Namespace packages](https://packaging.python.org/guides/creating-and-discovering-plugins/#using-namespace-packages), and thus, the package structure is essential.

   Please use the following Python package structure:
   ```
   nebulakit-myplugin/
      - README.md
      - setup.py
      - nebulakitplugins/
          - myplugin/
             - __init__.py
      - tests
          - __init__.py
   ```
   *NOTE:* the inner package `nebulakitplugins` DOES NOT have an `__init__.py` file.

3. The published packages have to be named `nebulakitplugins-{package-name}`, where `{package-name}` is a unique identifier for the plugin.

4. The setup.py file has to have the following template. You can use it as is by editing the TODO sections.

```python
from setuptools import setup

# TODO put the plugin name here
PLUGIN_NAME = "<plugin-name e.g. pandera>"

# TODO decide if the plugin is regular or `data`
# for regular plugins
microlib_name = f"nebulakitplugins-{PLUGIN_NAME}"
# For data/persistence plugins
# microlib_name = f"nebulakitplugins-data-{PLUGIN_NAME}"

# TODO add additional requirements
plugin_requires = ["nebulakit>=1.1.0b0,<2.0.0, "<other requirements>"]

__version__ = "0.0.0+develop"

setup(
    name=microlib_name,
    version=__version__,
    author="nebulaclouds",
    author_email="admin@nebula.org",
    # TODO Edit the description
    description="My awesome plugin.....",
    # TODO alter the last part of the following URL
    url="https://github.com/nebulaclouds/nebulakit/tree/master/plugins/nebulakit-...",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    namespace_packages=["nebulakitplugins"],
    packages=[f"nebulakitplugins.{PLUGIN_NAME}"],
    install_requires=plugin_requires,
    license="apache2",
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    # TODO OPTIONAL
    # FOR Plugins where auto-loading on installation is desirable, please uncomment this line and ensure that the
    # __init__.py has the right modules available to be loaded, or point to the right module
    # entry_points={"nebulakit.plugins": [f"{PLUGIN_NAME}=nebulakitplugins.{PLUGIN_NAME}"]},
)
```
5. Each plugin should have a README.md, which describes how to install it with a simple example. For example, refer to nebulakit-greatexpectations' [README](./nebulakit-greatexpectations/README.md).

6. Each plugin should have its own tests' package. *NOTE:* `tests` folder should have an `__init__.py` file.

7. There may be some cases where you might want to auto-load some of your modules when the plugin is installed. This is especially true for `data-plugins` and `type-plugins`.
In such a case, you can add a special directive in the `setup.py` which will instruct Nebulakit to automatically load the prescribed modules.

   Following shows an excerpt from the `nebulakit-data-fsspec` plugin's setup.py file.

    ```python
    setup(
        entry_points={"nebulakit.plugins": [f"{PLUGIN_NAME}=nebulakitplugins.{PLUGIN_NAME}"]},
    )

    ```

### Nebulakit Version Pinning
Currently we advocate pinning to minor releases of nebulakit. To bump the pins across the board, `cd plugins/` and then
update the command below with the appropriate range and run

```bash
for f in $(ls **/setup.py); do sed -i "s/nebulakit>.*,<1.1/nebulakit>=1.1.0b0,<1.2/" $f; done
```

Try using `gsed` instead of `sed` if you are on a Mac. Also this only works of course for setup files that start with the version in your sed command. There may be plugins that have different pins to start out with.

## References 📚
- Example of a simple Python task that allows adding only Python side functionality: [nebulakit-greatexpectations](./nebulakit-greatexpectations/)
- Example of a TypeTransformer or a Type Plugin: [nebulakit-pandera](./nebulakit-pandera/). These plugins add new types to Nebula and tell Nebula how to transform them and add additional features through types. Nebula is a multi-lang system, and type transformers allow marshaling between Nebulakit and backend and other languages.
- Example of TaskTemplate plugin which also allows plugin writers to supply a prebuilt container for runtime: [nebulakit-sqlalchemy](./nebulakit-sqlalchemy/)
- Example of a SQL backend plugin where the actual query invocation is done by a backend plugin: [nebulakit-snowflake](./nebulakit-snowflake/)
- Example of a Meta plugin that can wrap other tasks: [nebulakit-papermill](./nebulakit-papermill/)
- Example of a plugin that modifies the execution command: [nebulakit-spark](./nebulakit-spark/) OR [nebulakit-aws-sagemaker](./nebulakit-aws-sagemaker/)
- Example that allows executing the user container with some other context modifications: [nebulakit-kf-tensorflow](./nebulakit-kf-tensorflow/)
- Example of a Persistence Plugin that allows data to be stored to different persistence layers: [nebulakit-data-fsspec](./nebulakit-data-fsspec/)
