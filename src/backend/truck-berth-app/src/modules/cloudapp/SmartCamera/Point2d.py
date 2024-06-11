# automatically generated by the FlatBuffers compiler, do not modify

# namespace: SmartCamera

import flatbuffers
from flatbuffers.compat import import_numpy

np = import_numpy()


class Point2d(object):
    __slots__ = ["_tab"]

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Point2d()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsPoint2d(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)

    # Point2d
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Point2d
    def X(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # Point2d
    def Y(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0


def Point2dStart(builder):
    builder.StartObject(2)


def Start(builder):
    return Point2dStart(builder)


def Point2dAddX(builder, x):
    builder.PrependFloat32Slot(0, x, 0.0)


def AddX(builder, x):
    return Point2dAddX(builder, x)


def Point2dAddY(builder, y):
    builder.PrependFloat32Slot(1, y, 0.0)


def AddY(builder, y):
    return Point2dAddY(builder, y)


def Point2dEnd(builder):
    return builder.EndObject()


def End(builder):
    return Point2dEnd(builder)
