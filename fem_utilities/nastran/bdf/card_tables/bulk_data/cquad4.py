__author__ = 'Michael Redmond'

import tables
import numpy as np

from fem_utilities.nastran.bdf.card_readers import card_readers
from fem_utilities.nastran.bdf.card_tables.singleton_table import SingletonDecorator


#@SingletonDecorator
class CQUAD4(object):

    class DataTable(tables.IsDescription):
        EID = tables.Int32Col()
        table_type = tables.Int32Col()

    class DataTable1(tables.IsDescription):
        EID = tables.Int32Col()
        PID = tables.Int32Col()
        G1 = tables.Int32Col()
        G2 = tables.Int32Col()
        G3 = tables.Int32Col()
        G4 = tables.Int32Col()
        THETA = tables.Float64Col()
        ZOFFS = tables.Float64Col()
        BLANK = tables.StringCol(1)
        TFLAG = tables.Int32Col()
        T1 = tables.Float64Col()
        T2 = tables.Float64Col()
        T3 = tables.Float64Col()
        T4 = tables.Float64Col()
        field_width = tables.Int32Col()

    class DataTable2(tables.IsDescription):
        EID = tables.Int32Col()
        PID = tables.Int32Col()
        G1 = tables.Int32Col()
        G2 = tables.Int32Col()
        G3 = tables.Int32Col()
        G4 = tables.Int32Col()
        MCID = tables.Int32Col()
        ZOFFS = tables.Float64Col()
        BLANK = tables.StringCol(1)
        TFLAG = tables.Int32Col()
        T1 = tables.Float64Col()
        T2 = tables.Float64Col()
        T3 = tables.Float64Col()
        T4 = tables.Float64Col()
        field_width = tables.Int32Col()

    # noinspection PyUnresolvedReferences
    def __init__(self, h5file):
        super(CQUAD4, self).__init__()

        self.h5file = h5file

        self.data_group = self.h5file.add_bulk_data_group("CQUAD4", "CQUAD4 Data Group")

        self.data_table = self.h5file.create_table(self.data_group, "CQUAD4", self.DataTable, "CQUAD4 Data Table")
        self.data_table1 = self.h5file.create_table(self.data_group, "CQUAD4_1", self.DataTable1, "CQUAD4_1 Data Table")
        self.data_table2 = self.h5file.create_table(self.data_group, "CQUAD4_2", self.DataTable2, "CQUAD4_2 Data Table")

        self.data_row = self.data_table.row
        self.data_row1 = self.data_table1.row
        self.data_row2 = self.data_table2.row

    def reset_data1(self):
        self.data_row1['EID'] = -999999
        self.data_row1['PID'] = -999999
        self.data_row1['G1'] = -999999
        self.data_row1['G2'] = -999999
        self.data_row1['G3'] = -999999
        self.data_row1['G4'] = -999999
        self.data_row1['THETA'] = np.nan
        self.data_row1['ZOFFS'] = np.nan
        self.data_row1['BLANK'] = ""
        self.data_row1['TFLAG'] = -999999
        self.data_row1['T1'] = np.nan
        self.data_row1['T2'] = np.nan
        self.data_row1['T3'] = np.nan
        self.data_row1['T4'] = np.nan

    def reset_data2(self):
        self.data_row2['EID'] = -999999
        self.data_row2['PID'] = -999999
        self.data_row2['G1'] = -999999
        self.data_row2['G2'] = -999999
        self.data_row2['G3'] = -999999
        self.data_row2['G4'] = -999999
        self.data_row2['MCID'] = -999999
        self.data_row2['ZOFFS'] = np.nan
        self.data_row2['BLANK'] = ""
        self.data_row2['TFLAG'] = -999999
        self.data_row2['T1'] = np.nan
        self.data_row2['T2'] = np.nan
        self.data_row2['T3'] = np.nan
        self.data_row2['T4'] = np.nan

    def read_card(self, data):

        if len(data) >= 8 and isinstance(data[7], int):
            self._read_card2(data)
        else:
            self._read_card1(data)

    def _read_card1(self, data):
        self.reset_data1()

        self.data_row1['field_width'] = data[0]

        self.data_row1['EID'] = data[1]
        self.data_row1['PID'] = data[2]
        self.data_row1['G1'] = data[3]
        self.data_row1['G2'] = data[4]
        self.data_row1['G3'] = data[5]
        self.data_row1['G4'] = data[6]

        try:
            if data[7] != "":
                self.data_row1['THETA'] = data[7]

            if data[8] != "":
                self.data_row1['ZOFFS'] = data[8]

            self.data_row1['BLANK'] = data[9]

            if data[10] != "":
                self.data_row1['TFLAG'] = data[10]

            if data[11] != "":
                self.data_row1['T1'] = data[11]

            if data[12] != "":
                self.data_row1['T2'] = data[12]

            if data[13] != "":
                self.data_row1['T3'] = data[13]

            if data[14] != "":
                self.data_row1['T4'] = data[14]

        except IndexError:
            pass

        finally:
            self.h5file.append_data(self.data_row1, "ELEMENT", "CQUAD4", data[1])

            self.data_row['EID'] = data[1]
            self.data_row['table_type'] = 1
            self.h5file.append_data(self.data_row)

    def _read_card2(self, data):
        self.reset_data2()

        self.data_row2['field_width'] = data[0]

        self.data_row2['EID'] = data[1]
        self.data_row2['PID'] = data[2]
        self.data_row2['G1'] = data[3]
        self.data_row2['G2'] = data[4]
        self.data_row2['G3'] = data[5]
        self.data_row2['G4'] = data[6]

        try:
            if data[7] != "":
                self.data_row2['MCID'] = data[7]

            if data[8] != "":
                self.data_row2['ZOFFS'] = data[8]

            self.data_row2['BLANK'] = data[9]

            if data[10] != "":
                self.data_row2['TFLAG'] = data[10]

            if data[11] != "":
                self.data_row2['T1'] = data[11]

            if data[12] != "":
                self.data_row2['T2'] = data[12]

            if data[13] != "":
                self.data_row2['T3'] = data[13]

            if data[14] != "":
                self.data_row2['T4'] = data[14]

        except IndexError:
            pass

        finally:
            self.h5file.append_data(self.data_row2, "ELEMENT", "CQUAD4", data[1])

            self.data_row['EID'] = data[1]
            self.data_row['table_type'] = 2
            self.h5file.append_data(self.data_row)


card_readers['CQUAD4'] = SingletonDecorator(CQUAD4)