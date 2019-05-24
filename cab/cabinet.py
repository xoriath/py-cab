
import os.path

import cab.data
import cab.file
import cab.folder
import cab.header

class Cabinet:

    def __init__(self, buffer):
        self.buffer = buffer
        self.header = header.create(buffer)
        self.folders = list(cab.folder.create_folders(self.header, buffer))
        self.files = list(cab.file.create_files(self.header, buffer))

        self.folder_and_files = list(( (f, list(self._find_files_in_folder(f)) ) for f in self.folders))

        self.folder_and_datas = list(( (f, files, list(cab.data.create_datas(self.header, f, buffer)) ) for (f, files) in self.folder_and_files))
        
    def _find_files_in_folder(self, f):
        for fi in self.files:
            if fi.folder_index == f.index:
                yield fi

def open_cab(path):

    cab = read_cab(path)
    if not cab.header.has_next_cabinet and not cab.header.has_previous_cabinet:
        return cab

    set_id = cab.header.set_id
    cabinets = {
        cab.header.sequence: cab
    }

    current_dir = os.path.dirname(path)
    current_cab = cab
    while current_cab.header.has_previous_cabinet:
        current_cab = read_cab(os.path.join(current_dir, current_cab.header.previous_cabinet))
        cabinets[current_cab.header.sequence] = current_cab

    while current_cab.header.has_next_cabinet:
        current_cab = read_cab(os.path.join(current_dir, current_cab.header.next_cabinet))
        cabinets[current_cab.header.sequence] = current_cab

    return cabinets


def read_cab(path):
    with open(path, 'rb') as f:
        buffer = f.read()
        return Cabinet(buffer)
