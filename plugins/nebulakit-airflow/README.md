# Nebulakit Airflow Plugin
Airflow plugin allows you to seamlessly run Airflow tasks in the Nebula workflow without changing any code.

- Compile Airflow tasks to Nebula tasks
- Use Airflow sensors/operators in Nebula workflows
- Add support running Airflow tasks locally without running a cluster

## Example
```python
from airflow.sensors.filesystem import FileSensor
from nebulakit import task, workflow

@task()
def t1():
    print("nebula")


@workflow
def wf():
    sensor = FileSensor(task_id="id", filepath="/tmp/1234")
    sensor >> t1()


if __name__ == '__main__':
    wf()
```


To install the plugin, run the following command:

```bash
pip install nebulakitplugins-airflow
```
