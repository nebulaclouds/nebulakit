# Nebulakit Kubernetes Pod Plugin

By default, Nebula tasks decorated with `@task` are essentially single functions that are loaded in one container. But often, there is a need to run a job with more than one container.

In this case, a regular task is not enough. Hence, Nebula provides a Kubernetes pod abstraction to execute multiple containers, which can be accomplished using Pod's `task_config`. The `task_config` can be leveraged to fully customize the pod spec used to run the task.

To install the plugin, run the following command:

```bash
pip install nebulakitplugins-pod
```

An [example](https://docs.nebula.org/projects/cookbook/en/latest/auto/integrations/kubernetes/pod/pod.html) can be found in the documentation.
