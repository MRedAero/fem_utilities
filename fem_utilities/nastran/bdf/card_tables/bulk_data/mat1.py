__author__ = 'Michael Redmond'

import tables
import numpy as np

from fem_utilities.nastran.bdf.card_readers import card_readers
from fem_utilities.nastran.bdf.card_tables.singleton_table import SingletonDecorator


#@SingletonDecorator
class MAT1(object):

    class DataTable(tables.IsDescription):
        MID = tables.Int32Col()
        E = tables.Float64Col()
        G = tables.Float64Col()
        NU = tables.Float64Col()
        RHO = tables.Float64Col()
        A = tables.Float64Col()
        TREF = tables.Float64Col()
        ST = tables.Float64Col()
        SC = tables.Float64Col()
        SS = tables.Float64Col()
        MCSID = tables.Int32Col()
        field_width = tables.Int32Col()

    # noinspection PyUnresolvedReferences
    def __init__(self, h5file):
        super(MAT1, self).__init__()

        self.h5file = h5file

        self.data_group = self.h5file.add_bulk_data_group("MAT1", "MAT1 Data Group")

        self.data_table = self.h5file.create_table(self.data_group, "MAT1", self.DataTable, "MAT1 Data Table")

        self.data_row = self.data_table.row

    def reset_data(self):
        self.data_row['MID'] = -999999
        self.data_row['E'] = np.nan
        self.data_row['G'] = np.nan
        self.data_row['NU'] = np.nan
        self.data_row['RHO'] = np.nan
        self.data_row['A'] = np.nan
        self.data_row['TREF'] = np.nan
        self.data_row['ST'] = np.nan
        self.data_row['SC'] = np.nan
        self.data_row['SS'] = np.nan
        self.data_row['MCSID'] = -999999

    def read_card(self, data):
        self.reset_data()

        data_row = self.data_row

        data_row['field_width'] = data[0]

        data_row['MID'] = data[1]

        try:

            if data[2] != "":
                data_row['E'] = data[2]

            if data[3] != "":
                data_row['G'] = data[3]

            if data[4] != "":
                data_row['NU'] = data[4]

            if data[5] != "":
                data_row['RHO'] = data[5]

            if data[6] != "":
                data_row['A'] = data[6]

            if data[7] != "":
                data_row['TREF'] = data[7]

            if data[8] != "":
                data_row['ST'] = data[8]

            if data[9] != "":
                data_row['SC'] = data[9]

            if data[10] != "":
                data_row['SS'] = data[10]

            if data[11] != "":
                data_row['MCSID'] = data[11]

        except IndexError:
            pass
        finally:
            self.h5file.append_data(data_row, "MATERIAL", "MAT1", data[1])


card_readers['MAT1'] = SingletonDecorator(MAT1)