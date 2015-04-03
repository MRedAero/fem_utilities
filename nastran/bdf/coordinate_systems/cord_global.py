__author__ = 'Michael Redmond'

import numpy as np
from math import radians, cos, sin

from cord_abstract import CORDAbstract


# noinspection PyPep8Naming
class CORDGlobal(CORDAbstract):

    def __init__(self, parent):
        super(CORDGlobal, self).__init__(parent)

    def to_global(self, x, y=None, z=None):
        if y is None or z is None:
            return x

        return [x, y, z]