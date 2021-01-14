from abc import abstractmethod, ABC
from collections import UserDict
from typing import Union
from Utilities.__conf import _ArchTypeConf


class FactoryType(UserDict, ABC):

    def __setitem__(self, key: Union[str, None], value: object):
        if self._evaluate(value):
            super(FactoryType, self).__setitem__(key, value)
        else:
            raise ValueError(f"{value} is not supported")

    def __getitem__(self, key):
        if super(FactoryType, self).__contains__(key):
            return super(FactoryType, self).__getitem__(key)
        else:
            raise KeyError(f"{key} is not supported")

    def _evaluate(self, value: object):
        """ evaluates which objects are supported """
        if hasattr(self, '_instance'):
            return isinstance(value, self._instance)
        else:
            return hasattr(value, '__dict__')

    def _set_evaluator(self, *obj):
        """ sets objects in the evaluation """
        self._instance = obj


class ArchiveFileType(ABC):

    @abstractmethod
    def __init__(self):
        self.pth = None
        self.pwd = None
        self.fmt = None
        self.mbr = None
        self.new = None
        self.fmt = None


class ArchiverType(ABC):

    def __init__(self):
        self._r = 'r'
        self._w = 'w'

    def extract(self, archive: ArchiveFileType):
        return self._extract_method(archive)

    def compatible_with(self, archive: ArchiveFileType) -> bool:
        return self._is(archive)

    def inspect(self, archive: ArchiveFileType) -> list:
        return self._inspect_method(archive)

    def size(self, archive: ArchiveFileType):
        return self._size_method(archive)

    def _set_mode(self, option: str, read_or_write: bool):
        mode = 'read' if read_or_write else 'write'
        if option in _ArchTypeConf[mode].keys():
            if read_or_write:
                self._r = option
            else:
                self._w = option
        else:
            raise ValueError(f"'{option}' is not an available mode. "
                             f"Use supported_modes to get information about "
                             f"the available modes")

    def _get_mode(self, read_or_write: bool) -> str:
        return self._r if read_or_write else self._w

    @property
    def _mode_info(self):
        return _ArchTypeConf

    @abstractmethod
    def _size_method(self, archive: ArchiveFileType): ...

    @abstractmethod
    def _inspect_method(self, archive: ArchiveFileType): ...

    @abstractmethod
    def _extract_method(self, archive: ArchiveFileType): ...

    @abstractmethod
    def _is(self, archive: ArchiveFileType): ...


class ArchiveFindType(ArchiverType):
    """ Subclass which points to the appropriate ArchiverType class """

    def __init__(self, factory: FactoryType):
        super(ArchiveFindType, self).__init__()
        self.factory = factory

    @abstractmethod
    def get_val(self, archive: ArchiveFileType): ...

    @abstractmethod
    def get_key(self, archive: ArchiveFileType): ...

    def _extract_method(self, archive: ArchiveFileType):
        func = self.get_val(archive)
        return func._extract_method(archive)

    def _inspect_method(self, archive: ArchiveFileType):
        func = self.get_val(archive)
        return func._inspect_method(archive)

    def _size_method(self, archive: ArchiveFileType):
        func = self.get_val(archive)
        return func._size_method(archive)

    def _is(self, archive: ArchiveFileType): ...

