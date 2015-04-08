__author__ = 'Michael Redmond'

from fem_utilities.nastran.bdf.reader import BDFReader

if __name__ == '__main__':
    reader = BDFReader(r"D:\nastran\rotor.bdf")
    reader.read_bdf()