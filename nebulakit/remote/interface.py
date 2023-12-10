from nebulakit.models import interface as _interface_models


class TypedInterface(_interface_models.TypedInterface):
    @classmethod
    def promote_from_model(cls, model):
        """
        :param nebulakit.models.interface.TypedInterface model:
        :rtype: TypedInterface
        """
        return cls(model.inputs, model.outputs)
