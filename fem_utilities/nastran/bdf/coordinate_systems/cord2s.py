__author__ = 'Michael Redmond'

from math import radians, cos, sin

from cord_abstract import CORDAbstract


# noinspection PyPep8Naming
class CORD2S(CORDAbstract):
    """Defines a spherical coordinate system using the coordinates of three points.

    """

    def __init__(self, parent):
        super(CORD2S, self).__init__(parent)

    def to_reference(self, r, theta=None, phi=None):
        if type(r) is list:
            theta = r[1]
            phi = r[2]
            r = r[0]

        theta = radians(theta)
        phi = radians(phi)

        x = r*cos(theta)*sin(phi)
        y = r*sin(theta)*sin(phi)
        z = r*cos(phi)

        p = x*self._v1 + y*self._v2 + z*self._v3

        return [self.A1 + p[0], self.A2 + p[1], self.A3 + p[2]]

    def to_global(self, r, theta=None, phi=None):
        xyz = self.to_reference(r, theta, phi)

        if self.RID == 0:
            return xyz

        return self.parent.coords[self.RID].to_global(xyz)