import os
from os import PathLike
from functools import wraps
from typing import Optional, List, Union, Any
from Utilities.input.archive.factory import factory
from Utilities.base import ArchiveFileType


class FileException(Exception):

    def __init__(self, file: PathLike, message="is not a File"):
        self.file = file
        self.message = message
        super(FileException, self).__init__(self.message)

    def __str__(self):
        return f"Path '{self.file}' {self.message}"


class ArchiveFile(ArchiveFileType):

    def __init__(self, file: Union[str, PathLike],
                 pwd: Optional[Any] = None):
        super(ArchiveFile, self).__init__()

        if os.path.isfile(file):
            self.pth = os.path.abspath(file)
        else:
            raise FileException(file)

        self.new = os.path.abspath(os.path.join(self.pth, os.pardir))
        self.pwd = pwd

    def extractor(func):
        """ Method Extraction Decorator """
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            extractor = factory[self.format]
            method = func.__name__
            return extractor.__getattribute__(method)(self)
        return wrapper

    def set_read_mode(self, option: bool):
        extractor = factory[self.format]
        return extractor.set_read_mode(option)

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
    def supported_formats(self) -> str:
        return str(factory)

    @extractor
    def extract(self, members: Optional[List[str]] = None,
                to_path: Optional[PathLike] = None):
        self.mbr = members
        self.new = to_path if to_path else self.new

    @property
    @extractor
    def inspect(self): return None

    @property
    @extractor
    def size(self): return None
