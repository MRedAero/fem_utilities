__author__ = 'Michael Redmond'

import tables
import numpy as np

from fem_utilities.nastran.bdf.card_readers import card_readers
from fem_utilities.nastran.bdf.card_tables.singleton_table import SingletonDecorator


#@SingletonDecorator
class CORD2C(object):

    class DataTable(tables.IsDescription):
        CID = tables.Int32Col()
        RID = tables.Int32Col()
        A1 = tables.Float64Col()
        A2 = tables.Float64Col()
        A3 = tables.Float64Col()
        B1 = tables.Float64Col()
        B2 = tables.Float64Col()
        B3 = tables.Float64Col()
        C1 = tables.Float64Col()
        C2 = tables.Float64Col()
        C3 = tables.Float64Col()
        field_width = tables.Int32Col()

    def __init__(self, h5file):
        super(CORD2C, self).__init__()

        self.h5file = h5file

        self.data_group = self.h5file.add_bulk_data_group("CORD2C", "CORD2C Data Group")

        self.data_table = self.h5file.create_table(self.data_group, "CORD2C", self.DataTable, "CORD2C Data Table")

        self.data_row = self.data_table.row

    def reset_data(self):
        self.data_row['CID'] = -999999
        self.data_row['RID'] = -999999
        self.data_row['A1'] = np.nan
        self.data_row['A2'] = np.nan
        self.data_row['A3'] = np.nan
        self.data_row['B1'] = np.nan
        self.data_row['B2'] = np.nan
        self.data_row['B3'] = np.nan
        self.data_row['C1'] = np.nan
        self.data_row['C2'] = np.nan
        self.data_row['C3'] = np.nan

    def read_card(self, data):

        self.reset_data()

        self.data_row['field_width'] = data[0]

        self.data_row['CID'] = data[1]
        self.data_row['RID'] = data[2]
        self.data_row['A1'] = data[3]
        self.data_row['A2'] = data[4]
        self.data_row['A3'] = data[5]
        self.data_row['B1'] = data[6]
        self.data_row['B2'] = data[7]
        self.data_row['B3'] = data[8]
        self.data_row['C1'] = data[9]
        self.data_row['C2'] = data[10]
        self.data_row['C3'] = data[11]

        self.h5file.append_data(self.data_row, "COORD", "CORD2C", data[1])


card_readers['CORD2C'] = SingletonDecorator(CORD2C)