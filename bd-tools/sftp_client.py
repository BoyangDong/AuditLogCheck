import paramiko
import traceback
import sys
import os
from . import File, Folder

class SFTPClient:
    def __init__(self, ip, user, pw, port=22):
        try:
            transport = paramiko.Transport((ip, port))
            transport.connect(username=user, password=pw)
            self.sftp = paramiko.SFTPClient.from_transport(transport)
            print('> Connected to %s' % (ip))
        except Exception as e:
            print('*** Caught exception: %s: %s' %(e.__class__, e))
            traceback.print_exc()
            try:
                    self.sftp.close()
            except:
                    pass
                    sys.exit(1)
        self.files = []

    def add(self, f):
        if isinstance(f, File):
            self.files.append(f)
        elif isinstance(f, Folder):
            self.files.extend(f.selected_files)

    def send(self, dest='', callback=None, confirm=True):
        # self.sftp.chdir(path=dest)
        for f in self.files:
            print (self.sftp.put(f.get_abs(),
                                os.path.join(dest, f.file),
                                callback=callback))
        self.files = []

    def chdir(self, dest=None):
        if dest:
            self.sftp.chdir(dest)

    def put(self, localpath, remotepath, callback=None, confirm=True):
        return self.sftp.put(localpath, remotepath, callback, confirm)

    def listdir(self, dest='.'):
        return self.sftp.listdir(dest)

    def close(self):
        self.sftp.close()


if __name__ == '__main__':
    #ftp = SFTPClient('10.60.3.20', 'sftpuser', 'sftpuser', 22)
    ftp = SFTPClient('204.90.88.37', 'jobrunner', 'f8iwnpkx', 22) 
    ftp.close()

