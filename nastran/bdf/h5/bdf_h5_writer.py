__author__ = 'Michael Redmond'

import tables


class BDFTable(tables.IsDescription):
    ID = tables.Int32Col()
    CARD = tables.StringCol(8)


class BDFH5Writer(object):
    def __init__(self, h5file, prefix):
        super(BDFH5Writer, self).__init__()

        self._file = None
        self._prefix = None

        self.nastran = None
        self.executive_control = None
        self.case_control = None
        self.bulk_data = None

        self.append_count = 0

        self.prefix = prefix
        self.file = h5file

        self._setup_hierarchy()

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        if isinstance(value, str):
            try:
                self._file = tables.open_file(value, mode="w", title="%s" % value)
                self._file.create_group("/", self._prefix, "%s Data" % self._prefix)
            except Exception:
                print "Unable to create h5 file %s!" % value
                return
        else:
            self._file = value

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        if value[:1] == "/":
            self._prefix = value[1:]
        else:
            self._prefix = value

    def _setup_hierarchy(self):

        NoSuchNodeError = tables.exceptions.NoSuchNodeError

        try:
            self.nastran = self.file.get_node("/" + self.prefix, "Nastran")
        except NoSuchNodeError:
            self.nastran = self.file.create_group("/" + self.prefix, "Nastran", "Nastran Data")

        try:
            self.executive_control = self.file.get_node(self.nastran, "ExecutiveControl")
        except NoSuchNodeError:
            self.executive_control = self.file.create_group(self.nastran, "ExecutiveControl", "Executive Control")

        try:
            self.case_control = self.file.get_node(self.nastran, "CaseControl")
        except NoSuchNodeError:
            self.case_control = self.file.create_group(self.nastran, "CaseControl", "Case Control")

        try:
            self.bulk_data = self.file.get_node(self.nastran, "BulkData")
        except NoSuchNodeError:
            self.bulk_data = self.file.create_group(self.nastran, "BulkData", "Bulk Data")

        self.card_tables = {}

        try:
            table = self.file.get_node(self.bulk_data, "CoordTable")
            self.card_tables['COORD'] = table
        except NoSuchNodeError:
            self.card_tables['COORD'] = self.create_table(self.bulk_data, "CoordTable", BDFTable, "Coord Table")

        try:
            table = self.file.get_node(self.bulk_data, "GridTable")
            self.card_tables['GRID'] = table
        except NoSuchNodeError:
            self.card_tables['GRID'] = self.create_table(self.bulk_data, "GridTable", BDFTable, "Grid Table")

        try:
            table = self.file.get_node(self.bulk_data, "ElementTable")
            self.card_tables['ELEMENT'] = table
        except NoSuchNodeError:
            self.card_tables['ELEMENT'] = self.create_table(self.bulk_data, "ElementTable", BDFTable, "Element Table")

        try:
            table = self.file.get_node(self.bulk_data, "PropertyTable")
            self.card_tables['PROPERTY'] = table
        except NoSuchNodeError:
            self.card_tables['PROPERTY'] = self.create_table(self.bulk_data, "PropertyTable", BDFTable, "Property Table")

        try:
            table = self.file.get_node(self.bulk_data, "MaterialTable")
            self.card_tables['MATERIAL'] = table
        except NoSuchNodeError:
            self.card_tables['MATERIAL'] = self.create_table(self.bulk_data, "MaterialTable", BDFTable, "Material Table")

        self.card_data = {"COORD": self.card_tables["COORD"].row,
                          "GRID": self.card_tables["GRID"].row,
                          "ELEMENT": self.card_tables["ELEMENT"].row,
                          "PROPERTY": self.card_tables["PROPERTY"].row,
                          "MATERIAL": self.card_tables["MATERIAL"].row}

    def add_bulk_data_group(self, group_name, description=""):
        try:
            group = self.file.get_node(self.bulk_data, group_name)
        except tables.exceptions.NoSuchNodeError:
            group = self.file.create_group(self.bulk_data, group_name, description)

        return group

    def create_table(self, parent_group, table_name, data_config, table_description):
        try:
            table = self.file.get_node(parent_group, table_name)
        except tables.exceptions.NoSuchNodeError:
            table = self.file.create_table(parent_group, table_name, data_config, table_description)

        return table

    def append_data(self, data_table, category=None, card_type=None, id=None):
        data_table.append()

        if category is not None:
            card_data = self.card_data[category]
            card_data['CARD'] = card_type
            card_data['ID'] = id
            card_data.append()

        self.append_count += 1

        if self.append_count == 10000:
            self.file.flush()
            self.append_count = 0

    def close(self):
        self.file.close()