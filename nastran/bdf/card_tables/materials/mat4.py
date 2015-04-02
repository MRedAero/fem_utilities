__author__ = 'Michael Redmond'

import tables
import numpy as np

from ...card_readers import card_readers
from ...card_tables.singleton_table import SingletonDecorator


#@SingletonDecorator
class MAT4(object):

    class DataTable(tables.IsDescription):
        MID = tables.Int32Col()
        K = tables.Float64Col()
        CP = tables.Float64Col()
        RHO = tables.Float64Col()
        H = tables.Float64Col()
        MU = tables.Float64Col()
        HGEN = tables.Float64Col()
        REFENTH = tables.Float64Col()
        TCH = tables.Float64Col()
        TDELTA = tables.Float64Col()
        QLAT = tables.Float64Col()
        field_width = tables.Int32Col()

    # noinspection PyUnresolvedReferences
    def __init__(self, h5file):
        super(MAT4, self).__init__()

        self.h5file = h5file

        self.data_group = self.h5file.add_bulk_data_group("MAT4", "MAT4 Data Group")

        self.data_table = self.h5file.create_table(self.data_group, "MAT4", self.DataTable, "MAT4 Data Table")

        self.data_row = self.data_table.row

    def reset_data(self):
        self.data_row['MID'] = -999999
        self.data_row['K'] = np.nan
        self.data_row['CP'] = np.nan
        self.data_row['RHO'] = np.nan
        self.data_row['H'] = np.nan
        self.data_row['MU'] = np.nan
        self.data_row['HGEN'] = np.nan
        self.data_row['REFENTH'] = np.nan
        self.data_row['TCH'] = np.nan
        self.data_row['TDELTA'] = np.nan
        self.data_row['QLAT'] = np.nan

    def read_card(self, data):
        self.reset_data()

        data_row = self.data_row

        data_row['field_width'] = data[0]

        data_row['MID'] = data[1]

        try:

            if data[2] != "":
                data_row['K'] = data[2]

            if data[3] != "":
                data_row['CP'] = data[3]

            if data[4] != "":
                data_row['RHO'] = data[4]

            if data[5] != "":
                data_row['H'] = data[5]

            if data[6] != "":
                data_row['MU'] = data[6]

            if data[7] != "":
                data_row['HGEN'] = data[7]

            if data[8] != "":
                data_row['REFENTH'] = data[8]

            if data[9] != "":
                data_row['TCH'] = data[9]

            if data[10] != "":
                data_row['TDELTA'] = data[10]

            if data[11] != "":
                data_row['QLAT'] = data[11]

        except IndexError:
            pass
        finally:
            self.h5file.append_data(data_row, "MATERIAL", "MAT4", data[1])


card_readers['MAT4'] = SingletonDecorator(MAT4)