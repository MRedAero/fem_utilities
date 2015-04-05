__author__ = 'Michael Redmond'

import tables
import numpy as np

from ....card_readers import card_readers
from ....card_tables.singleton_table import SingletonDecorator


#@SingletonDecorator
class PCOMP(object):

    class DataTable(tables.IsDescription):
        PID = tables.Int32Col()
        Z0 = tables.Float64Col()
        NSM = tables.Float64Col()
        SB = tables.Float64Col()
        FT = tables.StringCol(8)
        TREF = tables.Float64Col()
        GE = tables.Float64Col()
        LAM = tables.StringCol(8)
        field_width = tables.Int32Col()

    class PlyTable(tables.IsDescription):
        PID = tables.Int32Col()
        MIDi = tables.Int32Col()
        Ti = tables.Float64Col()
        THETAi = tables.Float64Col()
        SOUTi = tables.StringCol(8)

    # noinspection PyUnresolvedReferences
    def __init__(self, h5file):
        super(PCOMP, self).__init__()

        self.h5file = h5file

        self.data_group = self.h5file.add_bulk_data_group("PCOMP", "PCOMP Data Group")

        self.data_table = self.h5file.create_table(self.data_group, "PCOMP_data", self.DataTable, "PCOMP Data Table")

        self.ply_table = self.h5file.create_table(self.data_group, "PCOMP_Plies", self.PlyTable, "PCOMP Ply Data Table")

        self.data_row = self.data_table.row
        self.ply_row = self.ply_table.row

    def reset_data(self):
        self.data_row['PID'] = -999999
        self.data_row['Z0'] = np.nan
        self.data_row['NSM'] = np.nan
        self.data_row['SB'] = -999999
        self.data_row['FT'] = ""
        self.data_row['TREF'] = np.nan
        self.data_row['GE'] = np.nan
        self.data_row['LAM'] = ""

    def reset_ply_data(self):
        self.ply_row['PID'] = -999999
        self.ply_row['MIDi'] = -999999
        self.ply_row['Ti'] = np.nan
        self.ply_row['THETAi'] = np.nan
        self.ply_row['SOUTi'] = ""

    def read_card(self, data):
        self.reset_data()

        data_row = self.data_row
        ply_row = self.ply_row

        data_row['field_width'] = data[0]

        data_row['PID'] = data[1]
        data_row['Z0'] = data[2]

        if data[3] != "":
            data_row['NSM'] = data[3]

        data_row['SB'] = data[4]
        data_row['FT'] = data[5]
        data_row['TREF'] = data[6]
        data_row['GE'] = data[7]

        data_row['LAM'] = data[8]

        self.h5file.append_data(data_row)

        if data[0] == 16:
            skip = 0
        else:
            try:
                if data[13] == "":
                    skip = 4
                else:
                    skip = 0
            except IndexError:
                skip = 0

        pid = data[1]

        for i in xrange(9, len(data), 4+skip):
            self.reset_ply_data()
            ply_row['PID'] = pid
            count = 0
            try:
                if data[i] != "":
                    ply_row['MIDi'] = data[i]
                    count += 1

                if data[i+1] != "":
                    ply_row['Ti'] = data[i+1]
                    count += 1

                if data[i+2] != "":
                    ply_row['THETAi'] = data[i+2]
                    count += 1

                if data[i+3] != "":
                    ply_row['SOUTi'] = data[i+3]
                    count += 1
            finally:
                if count:
                    self.h5file.append_data(ply_row, "PROPERTY", "PCOMP", data[1])


card_readers['PCOMP'] = SingletonDecorator(PCOMP)