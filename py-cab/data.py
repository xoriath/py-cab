
import collections
from itertools import zip_longest
import logging
import struct

class Data:
    """Each CFDATA record describes some amount of compressed data. 
    
    The first CFDATA entry for each folder is located using CFFOLDER.coffCabStart. Subsequent 
    CFDATA records for this folder are contiguous. In a standard cabinet all the CFDATA entries 
    are contiguous and in the same order as the CFFOLDER entries that refer them.
    """

    data_tuple = collections.namedtuple('CabDataHeader', 'csum cbData cbUncomp')
    data_format = '<I2H'

    def __init__(self, buffer, offset, reserved_size):
        self.header = Data.data_tuple._make(struct.unpack_from(Data.data_format, buffer=buffer, offset=offset))

        reserved_start = offset + struct.calcsize(Data.data_format)
        reserved_end = reserved_start + reserved_size
        data_start = reserved_end
        data_end = data_start + self.raw_size

        self.reserved = buffer[reserved_start : reserved_end]
        self.raw_data = buffer[data_start : data_end]

        self.calculated_checksum = self._calculate_checksum()
        

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Parsed data: %s', self.__repr__())

    def __repr__(self):
        return '<Data checksum={cheksum} valid={valid} compressed={raw_size} uncompressed={uncompressed_size}>'.format(cheksum=self.checksum,
                                                                                                                       valid=self.valid(),
                                                                                                                       raw_size=self.raw_size,
                                                                                                                       uncompressed_size=self.uncompressed_size)

    @property 
    def raw_size(self):
        return self.header.cbData

    @property
    def checksum(self):
        return self.header.csum

    @property
    def uncompressed_size(self):
        return self.header.cbUncomp

    @property
    def size(self):
        return struct.calcsize(Data.data_format) + len(self.reserved) + len(self.raw_data)

    def valid(self):
        return self.checksum == self.calculated_checksum

    
    def _calculate_checksum(self):
        """ Calculate the checksum of the data and the partial header
        
        From https://msdn.microsoft.com/en-us/library/bb417343.aspx#chksum 
        """
        data_checksum = Data._compute_checksum(self.raw_data)
        partial_header = bytearray(struct.pack('<HH', self.raw_size, self.uncompressed_size))
        return Data._compute_checksum(partial_header, seed=data_checksum)


    @staticmethod
    def _compute_checksum(buffer, seed=0):
        accumulator = seed
        
        for group in Data.group_by(4, buffer):
            if group.count(None) == 0:
                accumulator ^= group[0] | group[1] << 8 |group[2] << 16 | group[3] << 24
            elif group.count(None) == 1:
                accumulator ^= group[0] << 16 | group[1] << 8 | group[2] << 0
            elif group.count(None) == 2:
                accumulator ^= group[0] << 8 | group[1]
            elif group.count(None) == 3:
                accumulator ^= group[0]

        return accumulator

    @staticmethod
    def group_by(n, iterable, padvalue=None):
        return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)


def create_datas(header, folder, buffer):
    offset = folder.first_data_entry_offset
    number_of_data = folder.number_of_data_entries
    reserved_size = header.reserved_in_data

    for _ in range(number_of_data):
        data = Data(buffer, offset, reserved_size)
        offset += data.size
        yield data
