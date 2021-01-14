import os
from os import PathLike
from typing import Optional, List, Union, Any, Dict
from Utilities.input.archive.factory import factory
from Utilities.base import ArchiveFileType


class FileException(Exception):

    def __init__(self, file: PathLike, message="is not a File"):
        self.file = file
        self.message = message
        super(FileException, self).__init__(self.message)

    def __str__(self):
        return f"Path '{self.file}' {self.message}"


class _ArchFileFormat(ArchiveFileType):

    def __init__(self, file):
        super(_ArchFileFormat, self).__init__()
        if os.path.isfile(file):
            self.pth = os.path.abspath(file)
        else:
            raise FileException(file)
        self.new = os.path.abspath(os.path.dirname(self.pth))

    @classmethod
    def extractor(cls, func):
        """ Method Extraction Decorator """
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            arch = self._get_archiver
            return arch.__getattribute__(func.__name__)(self)
        return wrapper

    @property
    def format(self) -> str:
        if not self.fmt:
            for key, cls in factory.items():
                if cls.compatible_with(self):
                    self.fmt = key
                    break
            else:
                raise ValueError('Format is not supported')
        return self.fmt

    def _set_mode(self, option: str, r_or_w: bool):
        extractor = factory[self.format]
        return extractor._set_mode(option, r_or_w)

    def _get_mode(self, r_or_w):
        extractor = factory[self.format]
        return extractor._get_mode(r_or_w)

    @property
    def _get_archiver(self):
        return factory[self.format]


class ArchiveFile(_ArchFileFormat):

    def __init__(self, file: Union[str, PathLike],
                 pwd: Optional[Any] = None):
        super(ArchiveFile, self).__init__(file)
        self.pwd = pwd

    def set_read_mode(self, option: str):
        return self._set_mode(option, True)

    def set_write_mode(self, option: str):
        return self._set_mode(option, False)

    @_ArchFileFormat.extractor
    def extract(self, members: Optional[List[str]] = None,
                to_path: Optional[PathLike] = None):
        self.mbr = members
        self.new = os.path.abspath(to_path) if to_path else self.new

    @property
    def read_mode(self) -> str:
        return self._get_mode(True)

    @property
    def write_mode(self) -> str:
        return self._get_mode(False)

    @property
    def supported_formats(self) -> str:
        return str(factory)

    @property
    def supported_modes(self) -> dict:
        arch = self._get_archiver
        return arch._mode_info

    @property
    @_ArchFileFormat.extractor
    def inspect(self) -> Union[list, None]:
        return None

    @property
    @_ArchFileFormat.extractor
    def size(self) -> Union[Dict[str, int], None]:
        return None
