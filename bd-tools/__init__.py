import platform
from .file import File
from .file import Folder
from .archive import Archive
from .config import env
from .mail import Mail
from .sftp_client import SFTPClient
from .errors import PathError

if platform.system() is 'Windows':
    from .mount_drive_windows import MountDrive
