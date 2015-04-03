__author__ = 'Michael Redmond'

from cord_abstract import CORDAbstract


# noinspection PyPep8Naming
class CORD2R(CORDAbstract):
    """Defines a rectangular coordinate system using the coordinates of three points.

    """

    def __init__(self, parent):
        super(CORD2R, self).__init__(parent)

    def to_reference(self, x, y=None, z=None):
        if type(x) is list:
            y = x[1]
            z = x[2]
            x = x[0]

        p = x*self._v1 + y*self._v2 + z*self._v3

        return [self.A1 + p[0], self.A2 + p[1], self.A3 + p[2]]

    def to_global(self, x, y=None, z=None):
        xyz = self.to_reference(x, y, z)

        if self.RID == 0:
            return xyz

        return self.parent.coords[self.RID].to_global(xyz)