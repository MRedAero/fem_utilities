__author__ = 'Michael Redmond'

import tables


class BDFTable(tables.IsDescription):
    ID = tables.Int32Col()
    CARD = tables.StringCol(8)


class BDFH5(object):
    def __init__(self, h5file, prefix):
        super(BDFH5, self).__init__()

        self.file = h5file
        self.prefix = prefix
        self.file = None

        self.nastran = None
        self.executive_control = None
        self.case_control = None
        self.bulk_data = None

        self.append_count = 0

        self._setup_hierarchy(h5file)

    def _setup_hierarchy(self, h5file):

        if self.file is None:
            self.file = h5file

        NoSuchNodeError = tables.exceptions.NoSuchNodeError

        try:
            self.nastran = self.file.get_node(self.prefix, "Nastran")
        except NoSuchNodeError:
            self.nastran = self.file.create_group(self.prefix, "Nastran", "Nastran Data")

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

        self.card_tables = {"COORD": self.create_table(self.bulk_data, "CoordsTable", BDFTable, "Coords Table"),
                            "GRID": self.create_table(self.bulk_data, "GridsTable", BDFTable, "Grids Table"),
                            "ELEMENT": self.create_table(self.bulk_data, "ElementsTables", BDFTable, "Elements Table"),
                            "PROPERTY": self.create_table(self.bulk_data, "PropertiesTable", BDFTable, "Properties Table"),
                            "MATERIAL": self.create_table(self.bulk_data, "MaterialsTable", BDFTable, "Materials Table")}

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