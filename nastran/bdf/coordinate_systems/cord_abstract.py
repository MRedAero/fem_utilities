__author__ = 'Michael Redmond'

import numpy as np
from math import radians, cos, sin


# noinspection PyPep8Naming
class CORDAbstract(object):
    """Defines a cylindrical coordinate system using the coordinates of three points.

    """

    def __init__(self, parent):
        super(CORDAbstract, self).__init__()

        self.parent = parent

        self.CID = None
        self.RID = 0
        self.A1 = 1.
        self.A2 = 0.
        self.A3 = 0.
        self.B1 = 0.
        self.B2 = 1.
        self.B3 = 0.
        self.C1 = 0.
        self.C2 = 0.
        self.C3 = 1.

        self._v1 = [1., 0., 0.]
        self._v2 = [0., 1., 0.]
        self._v3 = [0., 0., 1.]

    def set_data(self, data, cols=None):
        if isinstance(data, dict):
            self._set_data_dict(data)
        else:
            self._set_data_list(data, cols)

        self.calc_vectors()

    def _set_data_list(self, data, cols):
        self.CID = data[cols[0]]

        nan = np.nan

        _data = data[cols[1]]

        if _data > 0:
            self.RID = _data

        _data = data[cols[2]]

        if data['A1'] != nan:
            self.A1 = _data

        _data = data[cols[3]]

        if data['A2'] != nan:
            self.A2 = _data

        _data = data[cols[4]]

        if data['A3'] != nan:
            self.A3 = _data

        _data = data[cols[5]]

        if data['B1'] != nan:
            self.B1 = _data

        _data = data[cols[6]]

        if data['B2'] != nan:
            self.B2 = _data

        _data = data[cols[7]]

        if data['B3'] != nan:
            self.B3 = _data

        _data = data[cols[8]]

        if data['C1'] != nan:
            self.C1 = _data

        _data = data[cols[9]]

        if data['C2'] != nan:
            self.C2 = _data

        _data = data[cols[10]]

        if data['C3'] != nan:
            self.C3 = _data

    def _set_data_dict(self, data):
        self.CID = data['CID']

        nan = np.nan

        if data['RID'] > 0:
            self.RID = data['RID']

        if data['A1'] != nan:
            self.A1 = data['A1']

        if data['A2'] != nan:
            self.A2 = data['A2']

        if data['A3'] != nan:
            self.A3 = data['A3']

        if data['B1'] != nan:
            self.B1 = data['B1']

        if data['B2'] != nan:
            self.B2 = data['B2']

        if data['B3'] != nan:
            self.B3 = data['B3']

        if data['C1'] != nan:
            self.C1 = data['C1']

        if data['C2'] != nan:
            self.C2 = data['C2']

        if data['C3'] != nan:
            self.C3 = data['C3']

    def calc_vectors(self):
        self._v3 = np.array([self.B1 - self.A1, self.B2 - self.A2, self.B3 - self.A3])
        self._v3 /= np.sqrt(self._v3.dot(self._v3))

        self._v1 = np.array([self.C1 - self.A1, self.C2 - self.A2, self.C3 - self.A3])
        self._v1 /= np.sqrt(self._v1.dot(self._v1))

        self._v2 = np.cross(self._v3, self._v1)

        self._v1 = np.cross(self._v2, self._v3)