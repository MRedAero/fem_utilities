__author__ = 'Michael Redmond'


import tables
import logging
from collections import OrderedDict

from ..card_readers import card_readers
from ..utilities import convert_field
from .bdf_h5 import BDFH5


class BDFReader(object):
    def __init__(self, bdffilename):
        super(BDFReader, self).__init__()

        self.bdffilename = None
        self.bdffile = None

        self.h5filename = None
        self.h5file = None

        self.logfilename = None

        self.set_bdf_filename(bdffilename)

        self._level = 0

        self._card_keys = card_readers.keys()

    def set_bdf_filename(self, filename):

        self.bdffilename = filename

        self.h5filename = filename.replace('.bdf', '.h5')

        self.logfilename = filename.replace('.bdf', '.log')

    def read_bdf(self):

        try:
            self.h5file = tables.open_file(self.h5filename, mode="w", title="%s" % self.h5filename)
            self.h5file.create_group("/", "Model", "Model Data")
        except Exception:
            print "Unable to create h5 file %s!" % self.h5filename
            return

        self.h5file = BDFH5(self.h5file, "/Model")

        try:
            self.bdffile = open(self.bdffilename, "r")
        except Exception:
            print "Unable to open bdf file %s!" % self.bdffilename
            self.bdffilename = None
            self.bdffile = None
            self.h5file.close()
            return

        try:
            logging.basicConfig(filename=self.logfilename, level=logging.DEBUG, filemode='w')
        except Exception:
            print "Unable to create log file %s!" % self.logfilename
            self.logfilename = None
            self.h5file.close()
            self.bdffile.close()
            return

        try:
            self._read_bdf()
        finally:
            self.h5file.close()

    def _read_bdf(self, filename=None):

        if self._level == 0:
            bdffile = self.bdffile
            filename = self.bdffilename
        else:
            try:
                bdffile = open(filename, "r")
            except Exception:
                print "Unable to open include bdf file %s!" % filename
                return

        lines = bdffile.read()

        if '\n' in lines:
            lines = lines.split('\n')
        elif '\r\n' in lines:
            lines = lines.split('\r\n')

        bdffile.close()

        #cdef int i, j, continuations, line_size, goto

        line_size = len(lines)

        continuations = 0

        #goto = 0

        self._level += 1

        # goto's are used so that xrange can be used instead of while statement; must faster

        for i in xrange(line_size):

            #print i

            if continuations:
                continuations -= 1
                continue

            line = remove_comments(lines[i])

            if line[0:1] == "$":
                continue

            goto = 2

            if line[0:7] == 'INCLUDE':

                goto = 1

                include_line = line

                continuations = 0
                for j in xrange(i+1, line_size):
                    if include_line.count("'") == 2:
                        break

                    continuations += 1
                    include_line += remove_comments(lines[j])

            if goto == 1:  # can this be merged under the previous if statement?
                #print 'goto = 1'
                # noinspection PyUnboundLocalVariable
                include_file = include_line.split("'")[1]
                self._read_bdf(include_file)
                continue

            if goto == 2:
                #print 'goto = 2'
                card = line[0:8].strip()

                if r'*' in card:
                    field_width = 16
                else:
                    field_width = 8

                card = card.replace(r'*', '')

                #print card

                if card in self._card_keys:
                    card_line = '%-64s' % line[8:72]

                    bdf_line = i

                    # noinspection PyBroadException
                    try:
                        cont = line[72:81].strip()  # should it be 72:80?  I had a problem with this before
                    except Exception:
                        cont = ''

                    goto = 3

                    continuations = 0
                    for j in xrange(i+1, line_size):
                        line = remove_comments(lines[j])

                        if line[0:8].strip() == cont:
                            card_line += '%-64s' % line[8:72]
                            continuations += 1
                        else:
                            break

                        # noinspection PyBroadException
                        try:
                            cont = line[72:81].strip()  # should it be 72:80?  I had a problem with this before
                        except Exception:
                            cont = ''
                else:
                    logging.info("Card %s not supported." % card)

            if goto == 3:
                #print 'goto = 3'
                if ',' in card_line:
                    data = map(convert_field, parse_string(card_line, ','))
                else:
                    data = map(convert_field, parse_string_fixed_width(card_line, field_width))

                data.insert(0, field_width)

                try:
                    # noinspection PyUnboundLocalVariable,PyCallingNonCallable
                    card_reader = card_readers[card](self.h5file)
                    card_reader.read_card(data)
                except Exception:
                    # noinspection PyUnboundLocalVariable
                    print 'BDF %s: line %d: field_width = %d\n%s' % (filename, bdf_line+1, field_width, card_line)
                    raise

                #goto = 0

        self._level -= 1


def parse_string(in_str, parse):
    return in_str.split(parse)


import re


def parse_string_fixed_width(in_str, width):
    return re.findall('.{%d}' % width, in_str)


def remove_comments(line):
    index = line.find(r'$')
    if index < 1:
        index = len(line)

    return line[0:index]