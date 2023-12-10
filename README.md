<p align="center">
    <img src="https://raw.githubusercontent.com/nebulaclouds/static-resources/main/common/nebula_circle_gradient_1_4x4.png" alt="Nebula Logo" width="100">
</p>
<h1 align="center">
    Nebulakit Python
</h1>
<p align="center">
    Nebulakit Python is the Python SDK built on top of Nebula
</p>
<h3 align="center">
    <a href="plugins/README.md">Plugins</a>
    <span> · </span>
    <a href="https://docs.nebula.org/projects/nebulakit/en/latest/contributing.html">Contribution Guide</a>
</h3>

[![PyPI version fury.io](https://badge.fury.io/py/nebulakit.svg)](https://pypi.python.org/pypi/nebulakit/)
[![PyPI download day](https://img.shields.io/pypi/dd/nebulakit.svg)](https://pypi.python.org/pypi/nebulakit/)
[![PyPI download month](https://img.shields.io/pypi/dm/nebulakit.svg)](https://pypi.python.org/pypi/nebulakit/)
[![PyPI total download](https://static.pepy.tech/badge/nebulakit)](https://static.pepy.tech/badge/nebulakit)
[![PyPI format](https://img.shields.io/pypi/format/nebulakit.svg)](https://pypi.python.org/pypi/nebulakit/)
[![PyPI implementation](https://img.shields.io/pypi/implementation/nebulakit.svg)](https://pypi.python.org/pypi/nebulakit/)
[![Codecov](https://img.shields.io/codecov/c/github/nebulaclouds/nebulakit?style=plastic)](https://app.codecov.io/gh/nebulaclouds/nebulakit)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/nebulakit.svg)](https://pypi.python.org/pypi/nebulakit/)
[![Docs](https://readthedocs.org/projects/nebulakit/badge/?version=latest&style=plastic)](https://nebulakit.rtfd.io)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Slack](https://img.shields.io/badge/slack-join_chat-white.svg?logo=slack&style=social)](https://slack.nebula.org)

Nebulakit Python is the Python Library for easily authoring, testing, deploying, and interacting with Nebula tasks, workflows, and launch plans.

If you haven't explored Nebula yet, please refer to:
 - [Nebula homepage](https://nebula.org)
 - [Nebula core repository](https://github.com/nebulaclouds/nebula)

## 🚀 Quick Start

Nebulakit is the core extensible library to author Nebula workflows and tasks and interact with Nebula backend services.

### Installation

```bash
pip install nebulakit
```

### A Simple Example

```python
from nebulakit import task, workflow

@task(cache=True, cache_version="1", retries=3)
def sum(x: int, y: int) -> int:
    return x + y

@task(cache=True, cache_version="1", retries=3)
def square(z: int) -> int:
    return z*z

@workflow
def my_workflow(x: int, y: int) -> int:
    return sum(x=square(z=x), y=square(z=y))
```

## 📦 Resources
- [Learn Nebulakit by examples](https://nebulacookbook.readthedocs.io/)
- [Nebulakit API documentation](https://nebulakit.readthedocs.io/)


## 📖 How to Contribute to Nebulakit
You can find the detailed contribution guide [here](https://docs.nebula.org/projects/nebulakit/en/latest/contributing.html). Plugins' contribution guide is included as well.

## Code Structure
Please see the [contributor's guide](https://docs.nebula.org/projects/nebulakit/en/latest/contributing.html) for a quick summary of how this code is structured.

## 🐞 File an Issue
Refer to the [issues](https://docs.nebula.org/en/latest/community/contribute.html#file-an-issue) section in the contribution guide if you'd like to file an issue.

## 🔌 Nebulakit Plugins
Refer to [plugins/README.md](plugins/README.md) for a list of available plugins.
There may be plugins outside of this list, but the core maintainers maintain this list.
