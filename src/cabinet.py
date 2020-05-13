
import os.path
from functools import reduce
import operator

import data, cabfile, folder, header


class InvalidCabinet(Exception):
    pass

class InvalidFileAllocation(InvalidCabinet):
    pass

class EmptyFileName(InvalidCabinet):
    pass

class Cabinet:

    def __init__(self, buffer, verify_integrity=True):
        self.buffer = buffer
        self.header = header.create(buffer)
        self.folders = list(folder.create_folders(self.header, buffer))
        self.files = list(cabfile.create_files(self.header, buffer))
        self.datas = { folder: list(data.create_datas(self.header, folder, buffer)) for folder in self.folders }

        self.resolve()

        if verify_integrity:
            self.verify()
        
    def resolve(self):
        self.folder_and_files = [( folder, list(find_files_in_folder(self.files, folder)) ) for folder in self.folders]
        self.folder_and_datas = list(( (f, files, self.datas[f]) for (f, files) in self.folder_and_files))

    def verify(self):
        self.verify_all_files_allocated_to_folder()
        self.verify_filenames()

    def verify_all_files_allocated_to_folder(self):
        files_in_folders = reduce(operator.concat, [folder_and_files_list[1] for folder_and_files_list in self.folder_and_files], [])
        if len(self.files) != len(files_in_folders):
            files_without_folder = set(self.files).symmetric_difference(set(files_in_folders))
            raise InvalidFileAllocation(f"Files not allocated to a folder: {files_without_folder}")

    def verify_filenames(self):
        if any(not file.name for file in self.files):
            raise EmptyFileName("File with empty name in cabinet")

        
def find_files_in_folder(files, folder):
    for fi in files:
        if fi.folder_index == folder.index:
            yield fi

def open_cab(path):

    cab = read_cab(path)
    if not cab.header.has_next_cabinet and not cab.header.has_previous_cabinet:
        return cab

    cab = read_chained_cabs(cab, os.path.dirname(path))
    return cab

def read_chained_cabs(root_cab, current_dir):
    set_id = root_cab.header.set_id
    cabinet_map = {
        root_cab.header.sequence: root_cab
    }

    current_cab = root_cab
    while current_cab.header.has_previous_cabinet:
        current_cab = read_cab(os.path.join(current_dir, current_cab.header.previous_cabinet))
        if current_cab.header.set_id != set_id:
            pass # TODO: log
        else:
            cabinet_map[current_cab.header.sequence] = current_cab

    current_cab = root_cab
    while current_cab.header.has_next_cabinet:
        current_cab = read_cab(os.path.join(current_dir, current_cab.header.next_cabinet))
        if current_cab.header.set_id != set_id:
            pass # TODO: log
        else:
            cabinet_map[current_cab.header.sequence] = current_cab

    max_cabinet_index = max(cabinet_map.keys())
    cabinets = [None] * (max_cabinet_index + 1)
    for index, value in cabinet_map.items():
        cabinets[index] = value

    return merge_cabs(cabinets)

def merge_cabs(cabs):
    folders = []
    files = []
    datas = []
    for cab in cabs:
        if any(f.is_continued_from_previous for f in cab.files):
            print('Merge with previous', cab.header)
        if any(f.is_continued_to_next for f in cab.files):
            print('Continue to next', cab.header)
        if any(f.is_continued_from_previous_and_to_next for f in cab.files):
            print('Prev and next', cab.header)

        folders.extend(cab.folders)
        files.extend(cab.files)
        datas.extend(cab.datas)

    return folders, files, datas

def read_cab(path):
    with open(path, 'rb') as f:
        buffer = f.read()
        return Cabinet(buffer)
