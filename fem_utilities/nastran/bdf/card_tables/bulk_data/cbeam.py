__author__ = 'Michael Redmond'

import tables
import numpy as np

from fem_utilities.nastran.bdf.card_readers import card_readers
from fem_utilities.nastran.bdf.card_tables.singleton_table import SingletonDecorator


#@SingletonDecorator
class CBEAM(object):

    class DataTable(tables.IsDescription):
        EID = tables.Int32Col()
        table_type = tables.Int32Col()

    class DataTable1(tables.IsDescription):
        EID = tables.Int32Col()
        PID = tables.Int32Col()
        GA = tables.Int32Col()
        GB = tables.Int32Col()
        X1 = tables.Float64Col()
        X2 = tables.Float64Col()
        X3 = tables.Float64Col()
        OFFT = tables.StringCol(8)
        PA = tables.Int32Col()
        PB = tables.Int32Col()
        W1A = tables.Float64Col()
        W2A = tables.Float64Col()
        W3A = tables.Float64Col()
        W1B = tables.Float64Col()
        W2B = tables.Float64Col()
        W3B = tables.Float64Col()
        SA = tables.Int32Col()
        SB = tables.Int32Col()
        field_width = tables.Int32Col()

    class DataTable2(tables.IsDescription):
        EID = tables.Int32Col()
        PID = tables.Int32Col()
        GA = tables.Int32Col()
        GB = tables.Int32Col()
        X1 = tables.Float64Col()
        X2 = tables.Float64Col()
        X3 = tables.Float64Col()
        BIT = tables.Float64Col()
        PA = tables.Int32Col()
        PB = tables.Int32Col()
        W1A = tables.Float64Col()
        W2A = tables.Float64Col()
        W3A = tables.Float64Col()
        W1B = tables.Float64Col()
        W2B = tables.Float64Col()
        W3B = tables.Float64Col()
        SA = tables.Int32Col()
        SB = tables.Int32Col()
        field_width = tables.Int32Col()

    class DataTable3(tables.IsDescription):
        EID = tables.Int32Col()
        PID = tables.Int32Col()
        GA = tables.Int32Col()
        GB = tables.Int32Col()
        G0 = tables.Int32Col()
        BLANK1 = tables.StringCol(1)
        BLANK2 = tables.StringCol(1)
        OFFT = tables.StringCol(8)
        PA = tables.Int32Col()
        PB = tables.Int32Col()
        W1A = tables.Float64Col()
        W2A = tables.Float64Col()
        W3A = tables.Float64Col()
        W1B = tables.Float64Col()
        W2B = tables.Float64Col()
        W3B = tables.Float64Col()
        SA = tables.Int32Col()
        SB = tables.Int32Col()
        field_width = tables.Int32Col()

    class DataTable4(tables.IsDescription):
        EID = tables.Int32Col()
        PID = tables.Int32Col()
        GA = tables.Int32Col()
        GB = tables.Int32Col()
        G0 = tables.Int32Col()
        BLANK1 = tables.StringCol(1)
        BLANK2 = tables.StringCol(1)
        BIT = tables.Float64Col()
        PA = tables.Int32Col()
        PB = tables.Int32Col()
        W1A = tables.Float64Col()
        W2A = tables.Float64Col()
        W3A = tables.Float64Col()
        W1B = tables.Float64Col()
        W2B = tables.Float64Col()
        W3B = tables.Float64Col()
        SA = tables.Int32Col()
        SB = tables.Int32Col()
        field_width = tables.Int32Col()

    # noinspection PyUnresolvedReferences
    def __init__(self, h5file):
        super(CBEAM, self).__init__()

        self.h5file = h5file

        self.data_group = self.h5file.add_bulk_data_group("CBEAM", "CBEAM Data Group")

        self.data_table = self.h5file.create_table(self.data_group, "CBEAM", self.DataTable, "CBEAM Data Table")
        self.data_table1 = self.h5file.create_table(self.data_group, "CBEAM_1", self.DataTable1, "CBEAM_1 Data Table")
        self.data_table2 = self.h5file.create_table(self.data_group, "CBEAM_2", self.DataTable2, "CBEAM_2 Data Table")
        self.data_table3 = self.h5file.create_table(self.data_group, "CBEAM_3", self.DataTable3, "CBEAM_3 Data Table")
        self.data_table4 = self.h5file.create_table(self.data_group, "CBEAM_4", self.DataTable4, "CBEAM_4 Data Table")

        self.data_row = self.data_table.row
        self.data_row1 = self.data_table1.row
        self.data_row2 = self.data_table2.row
        self.data_row3 = self.data_table3.row
        self.data_row4 = self.data_table4.row

    def reset_data1(self):
        self.data_row1['EID'] = -999999
        self.data_row1['PID'] = -999999
        self.data_row1['GA'] = -999999
        self.data_row1['GB'] = -999999
        self.data_row1['X1'] = np.nan
        self.data_row1['X2'] = np.nan
        self.data_row1['X3'] = np.nan
        self.data_row1['OFFT'] = ""
        self.data_row1['PA'] = -999999
        self.data_row1['PB'] = -999999
        self.data_row1['W1A'] = np.nan
        self.data_row1['W2A'] = np.nan
        self.data_row1['W3A'] = np.nan
        self.data_row1['W1B'] = np.nan
        self.data_row1['W2B'] = np.nan
        self.data_row1['W3B'] = np.nan
        self.data_row1['SA'] = -999999
        self.data_row1['SB'] = -999999

    def reset_data2(self):
        self.data_row2['EID'] = -999999
        self.data_row2['PID'] = -999999
        self.data_row2['GA'] = -999999
        self.data_row2['GB'] = -999999
        self.data_row2['X1'] = np.nan
        self.data_row2['X2'] = np.nan
        self.data_row2['X3'] = np.nan
        self.data_row2['BIT'] = np.nan
        self.data_row2['PA'] = -999999
        self.data_row2['PB'] = -999999
        self.data_row2['W1A'] = np.nan
        self.data_row2['W2A'] = np.nan
        self.data_row2['W3A'] = np.nan
        self.data_row2['W1B'] = np.nan
        self.data_row2['W2B'] = np.nan
        self.data_row2['W3B'] = np.nan
        self.data_row2['SA'] = -999999
        self.data_row2['SB'] = -999999

    def reset_data3(self):
        self.data_row3['EID'] = -999999
        self.data_row3['PID'] = -999999
        self.data_row3['GA'] = -999999
        self.data_row3['GB'] = -999999
        self.data_row3['G0'] = -999999
        self.data_row3['OFFT'] = ""
        self.data_row3['PA'] = -999999
        self.data_row3['PB'] = -999999
        self.data_row3['W1A'] = np.nan
        self.data_row3['W2A'] = np.nan
        self.data_row3['W3A'] = np.nan
        self.data_row3['W1B'] = np.nan
        self.data_row3['W2B'] = np.nan
        self.data_row3['W3B'] = np.nan
        self.data_row3['SA'] = -999999
        self.data_row3['SB'] = -999999

    def reset_data4(self):
        self.data_row3['EID'] = -999999
        self.data_row3['PID'] = -999999
        self.data_row3['GA'] = -999999
        self.data_row3['GB'] = -999999
        self.data_row3['G0'] = -999999
        self.data_row3['BIT'] = -999999
        self.data_row3['PA'] = -999999
        self.data_row3['PB'] = -999999
        self.data_row3['W1A'] = np.nan
        self.data_row3['W2A'] = np.nan
        self.data_row3['W3A'] = np.nan
        self.data_row3['W1B'] = np.nan
        self.data_row3['W2B'] = np.nan
        self.data_row3['W3B'] = np.nan
        self.data_row3['SA'] = -999999
        self.data_row3['SB'] = -999999

    def read_card(self, data):

        if isinstance(data[5], float):
            if isinstance(data[8], str):
                self._read_card1(data)
            else:
                self._read_card2(data)
        else:
            if isinstance(data[8], str):
                self._read_card3(data)
            else:
                self._read_card4(data)

    def _read_card1(self, data):
        self.reset_data1()

        self.data_row1['field_width'] = data[0]

        self.data_row1['EID'] = data[1]
        self.data_row1['PID'] = data[2]
        self.data_row1['GA'] = data[3]
        self.data_row1['GB'] = data[4]
        self.data_row1['X1'] = data[5]
        self.data_row1['X2'] = data[6]
        self.data_row1['X3'] = data[7]

        try:
            if data[8] != "":
                self.data_row1['OFFT'] = data[8]

            if data[9] != "":
                self.data_row1['PA'] = data[9]

            if data[10] != "":
                self.data_row1['PB'] = data[10]

            if data[11] != "":
                self.data_row1['W1A'] = data[11]

            if data[12] != "":
                self.data_row1['W2A'] = data[12]

            if data[13] != "":
                self.data_row1['W3A'] = data[13]

            if data[14] != "":
                self.data_row1['W1B'] = data[14]

            if data[15] != "":
                self.data_row1['W2B'] = data[15]

            if data[16] != "":
                self.data_row1['W3B'] = data[16]

            if data[17] != "":
                self.data_row1['SA'] = data[17]

            if data[18] != "":
                self.data_row1['SB'] = data[18]

        except IndexError:
            pass

        finally:
            self.h5file.append_data(self.data_row1, "ELEMENT", "CBEAM", data[1])

            self.data_row['EID'] = data[1]
            self.data_row['table_type'] = 1
            self.h5file.append_data(self.data_row)

    def _read_card2(self, data):
        self.reset_data2()

        data_row = self.data_row2

        data_row['field_width'] = data[0]

        data_row['EID'] = data[1]
        data_row['PID'] = data[2]
        data_row['GA'] = data[3]
        data_row['GB'] = data[4]
        data_row['X1'] = data[5]
        data_row['X2'] = data[6]
        data_row['X3'] = data[7]

        try:
            if data[8] != "":
                data_row['BIT'] = data[8]

            if data[9] != "":
                data_row['PA'] = data[9]

            if data[10] != "":
                data_row['PB'] = data[10]

            if data[11] != "":
                data_row['W1A'] = data[11]

            if data[12] != "":
                data_row['W2A'] = data[12]

            if data[13] != "":
                data_row['W3A'] = data[13]

            if data[14] != "":
                data_row['W1B'] = data[14]

            if data[15] != "":
                data_row['W2B'] = data[15]

            if data[16] != "":
                data_row['W3B'] = data[16]

            if data[17] != "":
                data_row['SA'] = data[17]

            if data[18] != "":
                data_row['SB'] = data[18]

        except IndexError:
            pass

        finally:
            self.h5file.append_data(data_row, "ELEMENT", "CBEAM", data[1])

            self.data_row['EID'] = data[1]
            self.data_row['table_type'] = 2
            self.h5file.append_data(self.data_row)

    def _read_card3(self, data):
        self.reset_data3()

        data_row = self.data_row3

        data_row['field_width'] = data[0]

        data_row['EID'] = data[1]
        data_row['PID'] = data[2]
        data_row['GA'] = data[3]
        data_row['GB'] = data[4]
        data_row['G0'] = data[5]
        data_row['BLANK1'] = data[6]
        data_row['BLANK2'] = data[7]

        try:
            if data[8] != "":
                data_row['OFFT'] = data[8]

            if data[9] != "":
                data_row['PA'] = data[9]

            if data[10] != "":
                data_row['PB'] = data[10]

            if data[11] != "":
                data_row['W1A'] = data[11]

            if data[12] != "":
                data_row['W2A'] = data[12]

            if data[13] != "":
                data_row['W3A'] = data[13]

            if data[14] != "":
                data_row['W1B'] = data[14]

            if data[15] != "":
                data_row['W2B'] = data[15]

            if data[16] != "":
                data_row['W3B'] = data[16]

            if data[17] != "":
                data_row['SA'] = data[17]

            if data[18] != "":
                data_row['SB'] = data[18]

        except IndexError:
            pass

        finally:
            self.h5file.append_data(data_row, "ELEMENT", "CBEAM", data[1])

            self.data_row['EID'] = data[1]
            self.data_row['table_type'] = 3
            self.h5file.append_data(self.data_row)

    def _read_card4(self, data):
        self.reset_data4()

        data_row = self.data_row4

        data_row['field_width'] = data[0]

        data_row['EID'] = data[1]
        data_row['PID'] = data[2]
        data_row['GA'] = data[3]
        data_row['GB'] = data[4]
        data_row['G0'] = data[5]
        data_row['BLANK1'] = data[6]
        data_row['BLANK2'] = data[7]

        try:
            if data[8] != "":
                data_row['BIT'] = data[8]

            if data[9] != "":
                data_row['PA'] = data[9]

            if data[10] != "":
                data_row['PB'] = data[10]

            if data[11] != "":
                data_row['W1A'] = data[11]

            if data[12] != "":
                data_row['W2A'] = data[12]

            if data[13] != "":
                data_row['W3A'] = data[13]

            if data[14] != "":
                data_row['W1B'] = data[14]

            if data[15] != "":
                data_row['W2B'] = data[15]

            if data[16] != "":
                data_row['W3B'] = data[16]

            if data[17] != "":
                data_row['SA'] = data[17]

            if data[18] != "":
                data_row['SB'] = data[18]

        except IndexError:
            pass

        finally:
            self.h5file.append_data(data_row, "ELEMENT", "CBEAM", data[1])

            self.data_row['EID'] = data[1]
            self.data_row['table_type'] = 4
            self.h5file.append_data(self.data_row)


card_readers['CBEAM'] = SingletonDecorator(CBEAM)