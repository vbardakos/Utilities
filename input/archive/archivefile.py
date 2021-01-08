import os
from os import PathLike
from typing import Optional, List, Union, Any, Type
from Utilities.input.archive.factory import factory
from Utilities.types import ArchiveFileType


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

    def extract(self, members: Optional[List[str]] = None,
                to_path: Optional[PathLike] = None) -> None:
        self.mbr = members
        self.new = to_path if to_path else self.new
        extractor = factory[self.format]
        extractor.extract(self)

    @property
    def inspect(self):
        extractor = factory[self.format]
        return extractor.inspect(self)

    @property
    def format(self) -> str:
        for key, cls in factory.items():
            if cls.compatible_with(self):
                return key
        else:
            raise ValueError('Format is not supported')

    @property
    def supported_formats(self) -> str:
        return str(factory)