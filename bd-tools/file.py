import os
import sys
from .errors import PathError
import shutil


class File:
    def __init__(self, path):
        path = os.path.normpath(path)
        if os.path.isabs(path) and os.path.isfile(path):
            self.dir, self.file = os.path.split(path)
        else:
            print('** File does not exist **')
            raise PathError('File does not exist')
        self._deletion_confirmed = False

    def __repr__(self):
        return self.file

    def __str__(self):
        return self.__repr__()

    def get_abs(self):
        return os.path.join(self.dir, self.file)
    
    def copy_to(self, name):
        shutil.copy2(os.path.join(self.dir, self.file), name)

    def delete(self):
        self._deletion_confirmed = True

    def confirm_deletion(self):
        if self._deletion_confirmed is True:
            os.remove(os.path.join(self.dir, self.file))
            print('** REMOVED: %s' % (self.__repr__()))



class Folder:
    def __init__(self, path):
        path = os.path.normpath(path)
        if os.path.isabs(path) and os.path.isdir(path):
            self.dir = path
        else:
            print('** Folder does not exist **')
            raise PathError('Folder does not exist')
        self.selected_files = []


    def get_files(self):
        return os.listdir(self.dir)

    def select_file_by_name(self, name):
        self.selected_files.append(File(os.path.join(self.dir, name)))

    def select_file_by_partial_str(self, partial):
        for file in self.get_files():
            if partial in file:
                f = File(os.path.join(self.dir, file))
                self.selected_files.append(f)

    '''def select_file_by_date(self)
    **** to be created *****
    '''

    def delete_selected(self):
        for f in self.selected_files:
            f.delete()

    def confirm_deletion_selected(self):
        for f in self.selected_files:
            f.confirm_deletion()

