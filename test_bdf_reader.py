__author__ = 'Michael Redmond'

from nastran.bdf import BDFReader

if __name__ == '__main__':
    reader = BDFReader(r"D:\nastran\wing.bdf")
    reader.read_bdf()


