
import collections
import struct

class Data:

    data_tuple = collections.namedtuple('CabDataTuple', 'csum cbData cbUncomp')
    data_format = '<I2H'

    def __init__(self, buffer, offset, reserved_size):
        self.header = Data.data_tuple._make(struct.unpack_from(Data.data_format, buffer=buffer, offset=offset))

        reserved_start = offset + struct.calcsize(Data.data_format)
        reserved_end = reserved_start + reserved_size
        data_start = reserved_end
        data_end = data_start + self.raw_size

        self.reserved = buffer[reserved_start : reserved_end]
        self.raw_data = buffer[data_start : data_end]

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


def create_datas(header, folder, buffer):
    offset = folder.first_data_entry_offset
    number_of_data = folder.number_of_data_entries
    reserved_size = header.reserved_in_data

    for _ in range(number_of_data):
        data = Data(buffer, offset, reserved_size)
        offset += data.size
        yield data
