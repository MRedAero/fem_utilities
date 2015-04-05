__author__ = 'Michael Redmond'

import tables
import vtk

try:
    from ..coordinate_systems import CoordinateSystems
    from ..utilities import bdf_card_numbering
except ValueError:
    from nastran.bdf.coordinate_systems import CoordinateSystems
    from nastran.bdf.utilities import bdf_card_numbering


class BDFH5Reader(object):
    def __init__(self, h5file):
        super(BDFH5Reader, self).__init__()

        self._file = None
        self._filename = None
        self._nastran = None

        self._cards = {}
        self._card_tables = {}

        self._coords = CoordinateSystems()

        self._original_id = 0

        self.file = h5file

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        if isinstance(value, str):
            assert tables.is_pytables_file(value)
            try:
                self._file = tables.open_file(value, mode="r")
                self._filename = value
            except Exception:
                print "Unable to create h5 file %s!" % value
                return
        else:
            self._file = value

        self._nastran = self._find_nastran()

        if self._nastran is None:
            self.file.close()
            self._file = None
            print "Unable to find Nastran Data in %s!" % value
            return

        if not self._setup_hierarchy():
            self.file.close()
            self._file = None

        self.read_coordinate_systems()

    def _find_nastran(self):
        if self._file is None:
            return

        for group in self._file.walk_groups("/"):
            if group._v_name == "Nastran" and group._v_title == "Nastran Data":
                return group

        return None

    def _setup_hierarchy(self):

        NoSuchNodeError = tables.exceptions.NoSuchNodeError

        try:
            self.executive_control = self.file.get_node(self._nastran, "ExecutiveControl")
        except NoSuchNodeError:
            print "Cannot find Executive Control!"
            return False

        try:
            self.case_control = self.file.get_node(self._nastran, "CaseControl")
        except NoSuchNodeError:
            print "Cannot find Case Control!"
            return False

        try:
            self.bulk_data = self.file.get_node(self._nastran, "BulkData")
        except NoSuchNodeError:
            print "Cannot find Bulk Data!"
            return False

        self._card_tables = {}

        try:
            table = self.file.get_node(self.bulk_data, "CoordTable")
            self._card_tables['COORD'] = table
        except NoSuchNodeError:
            print "Cannot find CoordTable!"
            return False

        try:
            table = self.file.get_node(self.bulk_data, "GridTable")
            self._card_tables['GRID'] = table
        except NoSuchNodeError:
            print "Cannot find GridTable!"
            return False

        try:
            table = self.file.get_node(self.bulk_data, "ElementTable")
            self._card_tables['ELEMENT'] = table
        except NoSuchNodeError:
            print "Cannot find ElementTable!"
            return False

        try:
            table = self.file.get_node(self.bulk_data, "PropertyTable")
            self._card_tables['PROPERTY'] = table
        except NoSuchNodeError:
            print "Cannot find PropertyTable!"
            return False

        try:
            table = self.file.get_node(self.bulk_data, "MaterialTable")
            self._card_tables['MATERIAL'] = table
        except NoSuchNodeError:
            print "Cannot find MaterialTable!"
            return False

        return True

    def close(self):
        if self._file:
            self._file.close()
            self._file = None

    def read_coordinate_systems(self):
        self._coords.reset()

        self._read_coord_table('CORD2C')
        self._read_coord_table('CORD2S')
        self._read_coord_table('CORD2R')

    def _read_coord_table(self, coord_type):
        coords = self._coords

        try:
            coord_node = self.file.get_node(self.bulk_data, coord_type)
            coord_table = self.file.get_node(coord_node, coord_type)
        except tables.exceptions.NoSuchNodeError:
            return

        coldescrs = coord_table.coldescrs

        _cols = [coldescrs['CID']._v_pos,
                 coldescrs['RID']._v_pos,
                 coldescrs['A1']._v_pos,
                 coldescrs['A2']._v_pos,
                 coldescrs['A3']._v_pos,
                 coldescrs['B1']._v_pos,
                 coldescrs['B2']._v_pos,
                 coldescrs['B3']._v_pos,
                 coldescrs['C1']._v_pos,
                 coldescrs['C2']._v_pos,
                 coldescrs['C3']._v_pos]

        table_data = coord_table.read()

        add_coord = coords.add_coord

        for data in table_data:
            coord = add_coord(coord_type, data[_cols[0]])
            coord.set_data(data, _cols)

    def create_vtk_data(self):

        self._original_id = 0

        ugrid = vtk.vtkUnstructuredGrid()
        global_ids = vtk.vtkIntArray()
        global_ids.SetName("global_ids")
        ugrid.GetCellData().AddArray(global_ids)

        card_ids = vtk.vtkIntArray()
        card_ids.SetName("card_ids")
        ugrid.GetCellData().AddArray(card_ids)

        original_ids.SetName("original_ids")
        ugrid.GetCellData().AddArray(original_ids)

        points, nid_map = self._create_vtk_points(ugrid)

        ugrid.SetPoints(points)

        self._create_vtk_cbeam(ugrid, nid_map, "CBEAM_1")
        self._create_vtk_cbeam(ugrid, nid_map, "CBEAM_2")
        self._create_vtk_cbeam(ugrid, nid_map, "CBEAM_3")
        self._create_vtk_cbeam(ugrid, nid_map, "CBEAM_4")

        self._create_vtk_ctria3(ugrid, nid_map, "CTRIA3_1")
        self._create_vtk_ctria3(ugrid, nid_map, "CTRIA3_2")

        self._create_vtk_cquad4(ugrid, nid_map, "CQUAD4_1")
        self._create_vtk_cquad4(ugrid, nid_map, "CQUAD4_2")

        global_ids.Squeeze()
        card_ids.Squeeze()
        original_ids.Squeeze()

        return ugrid

    def _create_vtk_points(self, ugrid):
        points = vtk.vtkPoints()

        try:
            _node = self.file.get_node(self.bulk_data, "GRID")
            _table = self.file.get_node(_node, "GRID")
        except tables.exceptions.NoSuchNodeError:
            return points

        # order is
        # CD, CP, ID, PS, SEID, X1, X2, X3

        table_data = _table.read()

        nid_map = {}

        new_cell = vtk.vtkVertex
        cell_type = new_cell().GetCellType()

        global_ids = ugrid.GetCellData().GetArray("global_ids")
        card_ids = ugrid.GetCellData().GetArray("card_ids")
        original_ids = ugrid.GetCellData().GetArray("original_ids")

        bdf_numbering = bdf_card_numbering["GRID"]

        #print card_ids

        coords = self._coords.coords

        for i in xrange(len(table_data)):
            data = table_data[i]

            if data[1] > 0:
                coord_id = data[1]
                xyz = coords[coord_id].to_global([data[5], data[6], data[7]])
            else:
                xyz = [data[5], data[6], data[7]]

            _id = data[2]

            points.InsertNextPoint(xyz)
            nid_map[_id] = i

            cell = new_cell()
            ids = cell.GetPointIds()
            ids.SetId(0, i)
            ugrid.InsertNextCell(cell_type, ids)
            global_ids.InsertNextValue(_id)
            card_ids.InsertNextValue(bdf_numbering)

            original_ids.InsertNextValue(self._original_id)
            self._original_id += 1

        points.Squeeze()

        return points, nid_map

    def _create_vtk_cbeam(self, ugrid, nid_map, table_name):

        try:
            _node = self.file.get_node(self.bulk_data, "CBEAM")
            _table = self.file.get_node(_node, table_name)
        except tables.exceptions.NoSuchNodeError:
            return

        coldescrs = _table.coldescrs

        _cols = [coldescrs['EID']._v_pos,
                 coldescrs['GA']._v_pos,
                 coldescrs['GB']._v_pos]

        eid = _cols[0]
        ga = _cols[1]
        gb = _cols[2]

        table_data = _table.read()

        new_cell = vtk.vtkLine
        cell_type = new_cell().GetCellType()

        global_ids = ugrid.GetCellData().GetArray("global_ids")
        card_ids = ugrid.GetCellData().GetArray("card_ids")
        original_ids = ugrid.GetCellData().GetArray("original_ids")

        bdf_numbering = bdf_card_numbering["CBEAM"]

        for i in xrange(len(table_data)):
            data = table_data[i]

            _id = data[eid]

            cell = new_cell()
            ids = cell.GetPointIds()
            ids.SetId(0, nid_map[data[ga]])
            ids.SetId(1, nid_map[data[gb]])

            ugrid.InsertNextCell(cell_type, ids)
            global_ids.InsertNextValue(_id)
            card_ids.InsertNextValue(bdf_numbering)

            original_ids.InsertNextValue(self._original_id)
            self._original_id += 1

    def _create_vtk_ctria3(self, ugrid, nid_map, table_name):

        try:
            _node = self.file.get_node(self.bulk_data, "CTRIA3")
            _table = self.file.get_node(_node, table_name)
        except tables.exceptions.NoSuchNodeError:
            return

        coldescrs = _table.coldescrs

        _cols = [coldescrs['EID']._v_pos,
                 coldescrs['G1']._v_pos,
                 coldescrs['G2']._v_pos,
                 coldescrs['G3']._v_pos]

        eid = _cols[0]
        g1 = _cols[1]
        g2 = _cols[2]
        g3 = _cols[3]

        table_data = _table.read()

        new_cell = vtk.vtkTriangle
        cell_type = new_cell().GetCellType()

        global_ids = ugrid.GetCellData().GetArray("global_ids")
        card_ids = ugrid.GetCellData().GetArray("card_ids")
        original_ids = ugrid.GetCellData().GetArray("original_ids")

        bdf_numbering = bdf_card_numbering["CTRIA3"]

        for i in xrange(len(table_data)):
            data = table_data[i]

            _id = data[eid]

            cell = new_cell()
            ids = cell.GetPointIds()
            ids.SetId(0, nid_map[data[g1]])
            ids.SetId(1, nid_map[data[g2]])
            ids.SetId(2, nid_map[data[g3]])

            ugrid.InsertNextCell(cell_type, ids)
            global_ids.InsertNextValue(_id)
            card_ids.InsertNextValue(bdf_numbering)

            original_ids.InsertNextValue(self._original_id)
            self._original_id += 1

    def _create_vtk_cquad4(self, ugrid, nid_map, table_name):

        try:
            _node = self.file.get_node(self.bulk_data, "CQUAD4")
            _table = self.file.get_node(_node, table_name)
        except tables.exceptions.NoSuchNodeError:
            return

        coldescrs = _table.coldescrs

        _cols = [coldescrs['EID']._v_pos,
                 coldescrs['G1']._v_pos,
                 coldescrs['G2']._v_pos,
                 coldescrs['G3']._v_pos,
                 coldescrs['G4']._v_pos]

        eid = _cols[0]
        g1 = _cols[1]
        g2 = _cols[2]
        g3 = _cols[3]
        g4 = _cols[4]

        table_data = _table.read()

        new_cell = vtk.vtkQuad
        cell_type = new_cell().GetCellType()

        global_ids = ugrid.GetCellData().GetArray("global_ids")
        card_ids = ugrid.GetCellData().GetArray("card_ids")
        original_ids = ugrid.GetCellData().GetArray("original_ids")

        bdf_numbering = bdf_card_numbering["CQUAD4"]

        for i in xrange(len(table_data)):
            data = table_data[i]

            _id = data[eid]

            cell = new_cell()
            ids = cell.GetPointIds()
            ids.SetId(0, nid_map[data[g1]])
            ids.SetId(1, nid_map[data[g2]])
            ids.SetId(2, nid_map[data[g3]])
            ids.SetId(3, nid_map[data[g4]])

            ugrid.InsertNextCell(cell_type, ids)
            global_ids.InsertNextValue(_id)
            card_ids.InsertNextValue(bdf_numbering)

            original_ids.InsertNextValue(self._original_id)
            self._original_id += 1


if __name__ == '__main__':
    h5 = BDFH5Reader(r"D:/nastran/wing.h5")
    print h5.create_vtk_data()
    h5.close()