__author__ = 'Michael Redmond'

import tables
import numpy as np

from ....card_readers import card_readers
from ....card_tables.singleton_table import SingletonDecorator


#@SingletonDecorator
class PSHELL(object):

    class DataTable(tables.IsDescription):
        PID = tables.Int32Col()
        MID1 = tables.Int32Col()
        T = tables.Float64Col()
        MID2 = tables.Int32Col()
        I12T3 = tables.Float64Col()
        MID3 = tables.Int32Col()
        TST = tables.Float64Col()
        NSM = tables.Float64Col()
        Z1 = tables.Float64Col()
        Z2 = tables.Float64Col()
        MID4 = tables.Int32Col()
        field_width = tables.Int32Col()

    # noinspection PyUnresolvedReferences
    def __init__(self, h5file):
        super(PSHELL, self).__init__()

        self.h5file = h5file

        self.data_group = self.h5file.add_bulk_data_group("PSHELL", "PSHELL Data Group")

        self.data_table = self.h5file.create_table(self.data_group, "PSHELL", self.DataTable, "PSHELL Data Table")

        self.data_row = self.data_table.row

    def reset_data(self):
        self.data_row['PID'] = -999999
        self.data_row['MID1'] = -999999
        self.data_row['T'] = np.nan
        self.data_row['MID2'] = -999999
        self.data_row['I12T3'] = np.nan
        self.data_row['MID3'] = -999999
        self.data_row['TST'] = np.nan
        self.data_row['NSM'] = np.nan
        self.data_row['Z1'] = np.nan
        self.data_row['Z2'] = np.nan
        self.data_row['MID4'] = -999999

    def read_card(self, data):
        self.reset_data()

        data_row = self.data_row

        data_row['field_width'] = data[0]

        data_row['PID'] = data[1]

        try:

            if data[2] != "":
                data_row['MID1'] = data[2]

            if data[3] != "":
                data_row['I12T3'] = data[3]

            if data[4] != "":
                data_row['MID2'] = data[4]

            if data[5] != "":
                data_row['TST'] = data[5]

            if data[6] != "":
                data_row['NSM'] = data[6]

            if data[7] != "":
                data_row['Z1'] = data[7]

            if data[8] != "":
                data_row['Z2'] = data[8]

            if data[9] != "":
                data_row['MID4'] = data[9]

        except IndexError:
            pass
        finally:
            self.h5file.append_data(data_row, "PROPERTY", "PSHELL", data[1])


card_readers['PSHELL'] = SingletonDecorator(PSHELL)