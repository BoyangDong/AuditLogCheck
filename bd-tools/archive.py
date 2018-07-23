import os
from . import File, Folder
from zipfile import ZipFile
import zipfile
from .errors import PathError



class Archive:
    def __init__(self, dst, name):
        if not os.path.isdir(dst):
            raise PathError('destination path not found')
        self.fn = self.__get_name(dst, name)
        self.files = []


    def __get_name(self,dst, name):
        fn = os.path.join(dst, name)
        if not os.path.isfile(fn):
            return fn
        i = 1
        while True:
            base, ext = os.path.splitext(fn)
            temp_fn = '%s_%s%s' % (base,i,ext)
            if not os.path.isfile(temp_fn):
                return temp_fn
            i = i + 1
            
    def add(self, f):
        if isinstance(f, File):
            self.files.append(f)
        elif isinstance(f, Folder):
            self.files.extend(f.selected_files)


    def write(self, arc_folder=''):
        if len(self.files) == 0:
            return None

        zf = ZipFile(self.fn, 'w', compression=zipfile.ZIP_DEFLATED, allowZip64=True)
        for f in self.files:
            zf.write(f.get_abs(), os.path.join(arc_folder, f.file))
        if zf.testzip() is None:
            zf.printdir()
            zf.close()
            print(self.fn)
            return self.fn
        else:
            print('%s is a bad file' % zf.testzip())
            zf.close()
            return None

    def __verify(self):
        try:
            zf = ZipFile(self.fn, 'r', compression=zipfile.ZIP_DEFLATED, allowZip64=True)
        except:
            print('** zip file not found **')
            return False
        if zf.testzip():
            print('%s is a bad file' % zf.testzip())
            zf.close()
            return False
        lst = map(lambda f: os.path.basename(f), zf.namelist())
        for f in self.files:
            if f.file not in lst:
                print('missing file: %s' % (f))
                zf.close()
                return False
        zf.close()
        return True

    def write_and_delete_origin(self, arc_folder=''):
        fn = self.write(arc_folder)
        if fn is None:
            return None
        elif self.__verify():
            for f in self.files:
                f.delete()
                f.confirm_deletion()
        return fn


    




