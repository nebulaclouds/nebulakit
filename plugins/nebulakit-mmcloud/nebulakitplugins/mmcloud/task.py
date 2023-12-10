from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

from nebulakitplugins.mmcloud.utils import nebula_to_mmcloud_resources
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Struct

from nebulakit.configuration import SerializationSettings
from nebulakit.core.python_function_task import PythonFunctionTask
from nebulakit.core.resources import Resources
from nebulakit.extend import TaskPlugins
from nebulakit.image_spec.image_spec import ImageSpec


@dataclass
class MMCloudConfig(object):
    """
    Configures MMCloudTask. Tasks specified with MMCloudConfig will be executed using Memory Machine Cloud.
    """

    # This allows the user to specify additional arguments for the float submit command
    submit_extra: str = ""


class MMCloudTask(PythonFunctionTask):
    _TASK_TYPE = "mmcloud_task"

    def __init__(
        self,
        task_config: Optional[MMCloudConfig],
        task_function: Callable,
        container_image: Optional[Union[str, ImageSpec]] = None,
        requests: Optional[Resources] = None,
        limits: Optional[Resources] = None,
        **kwargs,
    ):
        super().__init__(
            task_config=task_config or MMCloudConfig(),
            task_type=self._TASK_TYPE,
            task_function=task_function,
            container_image=container_image,
            **kwargs,
        )

        self._mmcloud_resources = nebula_to_mmcloud_resources(requests=requests, limits=limits)

    def execute(self, **kwargs) -> Any:
        return PythonFunctionTask.execute(self, **kwargs)

    def get_custom(self, settings: SerializationSettings) -> Dict[str, Any]:
        """
        Return plugin-specific data as a serializable dictionary.
        """
        config = {
            "submit_extra": self.task_config.submit_extra,
            "resources": [str(resource) if resource else None for resource in self._mmcloud_resources],
        }
        s = Struct()
        s.update(config)
        return json_format.MessageToDict(s)


TaskPlugins.register_pythontask_plugin(MMCloudConfig, MMCloudTask)
