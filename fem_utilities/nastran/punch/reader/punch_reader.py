__author__ = 'Michael Redmond'

import os
import gc
import logging

import tables

from fem_utilities.nastran.punch.table_readers import table_readers


class PunchReader(object):
    def __init__(self, pchfilename):
        super(PunchReader, self).__init__()

        self.pchfilename = None
        self.pchfile = None

        self.h5filename = None
        self.h5file = None

        self.logfilename = None

        self.set_pch_filename(pchfilename)

        self.data_lines = None

        self.header_data = None

    def set_pch_filename(self, filename):

        self.pchfilename = filename

        self.h5filename = filename.replace(".pch", ".h5")

        self.logfilename = filename.replace(".pch", ".log")

    def get_table_reader(self, first):
        skip_i = 0
        data_lines = self.data_lines

        header_data = []

        for i in xrange(first, len(data_lines)):
            if data_lines[i][0] != "$":
                # the table's header data has ended
                break

            header_data.append(data_lines[i])

            skip_i += 1

        table_reader = None

        for i in xrange(len(table_readers)):
            table_reader_cls = table_readers[i]

            if table_reader_cls.matches_format(header_data):
                # the table format has been matched, and the table_reader will be initialized and returned
                table_reader = table_reader_cls(self.h5file, header_data)
                break

        self.header_data = header_data

        return table_reader, skip_i-1

    def skip_table(self, first):
        skip_i = 0
        data_lines = self.data_lines

        for i in xrange(first, len(data_lines)):
            if data_lines[i] == "" or data_lines[i][0] == "$":
                # the current table has ended
                break

            skip_i += 1

        if self.header_data is not None:
            header_format = ""
            for i in xrange(len(self.header_data)):
                header_format += self.header_data[i][:72].strip() + '\n'
            logging.info("Table not supported with the following format:\n%s", header_format)

        return skip_i-1

    def read_pch(self):

        try:
            self.h5file = tables.open_file(self.h5filename, mode="w", title="%s" % self.h5filename)
        except Exception:
            print "Unable to create h5 file %s!" % self.h5filename
            return

        try:
            self.pchfile = open(self.pchfilename, "rb")
        except Exception:
            print "Unable to open punch file %s!" % self.pchfilename
            self.pchfilename = None
            self.pchfile = None
            self.h5file.close()
            return

        try:
            logging.basicConfig(filename=self.logfilename, level=logging.DEBUG, filemode='w')
        except Exception:
            print "Unable to create log file %s!" % self.logfilename
            self.logfilename = None
            self.h5file.close()
            self.pchfile.close()
            return

        file_size = float(os.path.getsize(self.pchfilename))

        bytes_to_read = 100000000  # 100 megabytes

        if file_size % 81 == 0:
            # lines are separated by '\n'
            bytes_to_read -= bytes_to_read % 81
            line_separator = "\n"
        else:
            # lines are separated by '\r\n'
            bytes_to_read -= bytes_to_read % 82
            line_separator = "\r\n"

        bytes_read = 0

        skip_i = 0
        table_reader = None

        try:
            while True:

                fraction = min(100., 100.*float(bytes_read)/file_size)

                print "%6.2f" % fraction + "%"

                bytes_read += bytes_to_read

                # force garbage collection
                data = None
                self.data_lines = None
                data_lines = None
                gc.collect()

                data = self.pchfile.read(bytes_to_read)

                if data == "":
                    # no more data to read
                    break

                self.data_lines = data.split(line_separator)
                data_lines = self.data_lines

                for i in xrange(len(data_lines)):
                    if skip_i:
                        # these lines have already been read in sub-loops and need to be skipped here
                        skip_i -= 1
                        continue

                    if data_lines[i] == "":
                        # blank line
                        continue

                    if data_lines[i][0] == "$":
                        # new table has started, determine what it is and get the table_reader
                        table_reader, skip_i = self.get_table_reader(i)
                        continue

                    if table_reader is None:
                        # skip unsupported table
                        skip_i = self.skip_table(i)
                        continue

                    # read or continue reading the current table
                    skip_i = table_reader.read_table(i, data_lines)

        finally:
            # no matter what happens, close these files
            self.h5file.close()
            self.pchfile.close()