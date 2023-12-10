from nebulaidl.admin import common_pb2 as _common_pb2

from nebulakit.models import common as _common


class Sort(_common.NebulaIdlEntity):
    class Direction(object):
        DESCENDING = _common_pb2.Sort.DESCENDING
        ASCENDING = _common_pb2.Sort.ASCENDING

    def __init__(self, key, direction):
        """
        :param Text key: field to sort on
        :param int direction: From nebulakit.models.admin.common.Sort.Direction enum
        """
        self._key = key
        self._direction = direction

    @property
    def key(self):
        """
        :rtype: Text
        """
        return self._key

    @property
    def direction(self):
        """
        :rtype: int
        """
        return self._direction

    def to_nebula_idl(self):
        """
        :rtype: nebulaidl.admin.common_pb2.Sort
        """
        return _common_pb2.Sort(key=self.key, direction=self.direction)

    @classmethod
    def from_nebula_idl(cls, pb2_object):
        """
        :param nebulaidl.admin.common_pb2.Sort pb2_object:
        :rtype: Sort
        """
        return cls(key=pb2_object.key, direction=pb2_object.direction)

    @classmethod
    def from_python_std(cls, text):
        """
        :param Text text:
        :rtype: Sort
        """
        text = text.strip()
        if text[-1] != ")":
            raise ValueError(
                "Could not parse string.  Must be in format 'asc(key)' or 'desc(key)'.  '{}' did not "
                "end with ')'.".format(text)
            )
        if text.startswith("asc("):
            direction = Sort.Direction.ASCENDING
            key = text[len("asc(") : -1].strip()
        elif text.startswith("desc("):
            direction = Sort.Direction.DESCENDING
            key = text[len("desc(") : -1].strip()
        else:
            raise ValueError(
                "Could not parse string.  Must be in format 'asc(key)' or 'desc(key)'.  '{}' did not "
                "start with 'asc(' or 'desc'.".format(text)
            )
        return cls(key=key, direction=direction)
