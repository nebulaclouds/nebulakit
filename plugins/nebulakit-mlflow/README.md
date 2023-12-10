# Nebulakit MLflow Plugin

MLflow enables us to log parameters, code, and results in machine learning experiments and compare them using an interactive UI.
This MLflow plugin enables seamless use of MLFlow within Nebula, and render the metrics and parameters on Nebula Deck.

To install the plugin, run the following command:

```bash
pip install nebulakitplugins-mlflow
```

Example
```python
from nebulakit import task, workflow
from nebulakitplugins.mlflow import mlflow_autolog
import mlflow

@task(enable_deck=True)
@mlflow_autolog(framework=mlflow.keras)
def train_model():
    ...
```
