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

    def __init__(self, path):
        super(_ArchFileFormat, self).__init__()
        self.pth = path

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

    @property
    def _get_archiver(self):
        return factory[self.format]


class ArchiveFile(_ArchFileFormat):

    def __init__(self, file: Union[str, PathLike],
                 pwd: Optional[Any] = None):
        if os.path.isfile(file):
            self.pth = os.path.abspath(file)
        else:
            raise FileException(file)
        self.new = os.path.abspath(os.path.join(self.pth, os.pardir))
        self.pwd = pwd
        super(ArchiveFile, self).__init__(self.pth)

    def set_read_mode(self, option: bool):
        extractor = factory[self.format]
        return extractor.set_read_mode(option)

    @_ArchFileFormat.extractor
    def extract(self, members: Optional[List[str]] = None,
                to_path: Optional[PathLike] = None):
        self.mbr = members
        self.new = to_path if to_path else self.new

    @property
    def supported_formats(self) -> str:
        return str(factory)

    @property
    def mode_info(self):
        arch = self._get_archiver
        return arch.mode_info

    @property
    @_ArchFileFormat.extractor
    def inspect(self) -> Union[list, None]:
        return None

    @property
    @_ArchFileFormat.extractor
    def size(self) -> Union[Dict[str, int], None]:
        return None
