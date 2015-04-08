__author__ = 'Michael Redmond'

from cord_global import CORDGlobal
from cord2c import CORD2C
from cord2s import CORD2S
from cord2r import CORD2R


class CoordinateSystems(object):
    def __init__(self):
        super(CoordinateSystems, self).__init__()

        self.coords = None

        self.reset()

    def add_coord(self, coord_type, id):
        assert id not in self.coords

        self.coords[id] = globals()[coord_type](self)

        return self.coords[id]

    def reset(self):
        self.coords = {}

        self.coords["0"] = CORDGlobal(self)