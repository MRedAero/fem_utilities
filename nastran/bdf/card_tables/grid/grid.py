__author__ = 'Michael Redmond'

import tables
import numpy as np

from ...card_readers import card_readers
from ..singleton_table import SingletonDecorator


#@SingletonDecorator
class GRID(object):

    class DataTable(tables.IsDescription):
        ID = tables.Int32Col()
        CP = tables.Int32Col()
        X1 = tables.Float64Col()
        X2 = tables.Float64Col()
        X3 = tables.Float64Col()
        CD = tables.Int32Col()
        PS = tables.Int32Col()
        SEID = tables.Int32Col()
        field_width = tables.Int32Col()

    def __init__(self, h5file):
        super(GRID, self).__init__()

        self.h5file = h5file

        self.data_group = self.h5file.add_bulk_data_group("GRID", "GRID Data Group")

        self.data_table = self.h5file.create_table(self.data_group, "GRID", self.DataTable, "GRID Data Table")

        self.data_row = self.data_table.row

    def reset_data(self):
        self.data_row['ID'] = -999999
        self.data_row['CP'] = -999999
        self.data_row['X1'] = np.nan
        self.data_row['X2'] = np.nan
        self.data_row['X3'] = np.nan
        self.data_row['CD'] = -999999
        self.data_row['PS'] = -999999
        self.data_row['SEID'] = -999999

    def read_card(self, data):

        self.reset_data()

        self.data_row['field_width'] = data[0]

        self.data_row['ID'] = data[1]

        if data[2] != "":
            self.data_row['CP'] = data[2]

        self.data_row['X1'] = data[3]
        self.data_row['X2'] = data[4]
        self.data_row['X3'] = data[5]

        try:
            self.data_row['CD'] = data[6]
            self.data_row['PS'] = data[7]
            self.data_row['SEID'] = data[8]
        except TypeError:
            pass
        finally:
            self.h5file.append_data(self.data_row, "GRID", "GRID", data[1])


card_readers['GRID'] = SingletonDecorator(GRID)