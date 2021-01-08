from Utilities.types import FactoryType, ArchiveFileType, ArchiverType
from typing import Union
import json


class ArchiveFactory(FactoryType):

    def register(self, key: Union[str, None], archiver: object):
        super(ArchiveFactory, self).__setitem__(key, archiver)

    def set_config(self, config: dict):
        self.data = config

    def __str__(self):
        def _mapper(kv):
            k, v = kv
            return k, {'name': v.__class__.__name__, 'id': id(v)}

        dict_gen = map(_mapper, self.data.items())
        return json.dumps(dict(dict_gen), indent=2)


factory: ArchiveFactory


class ArchiveFinder(ArchiverType):

    def get_val(self, archive: ArchiveFileType) -> ArchiverType:
        return factory[self.get_key(archive)]

    @staticmethod
    def get_key(archive: ArchiveFileType) -> str:
        for item, func in factory.items():
            if func.combatible_with(archive.pth):
                return item
        else:
            raise KeyError(f"{archive.pth} Format is not compatible")

    def _extract_method(self, archive: ArchiveFileType):
        func = self.get_val(archive)
        return func._extract_method(archive)

    def _inspect_method(self, archive: ArchiveFileType):
        func = self.get_val(archive)
        return func._inspect_method(archive)

    def _size_method(self, archive: ArchiveFileType):
        pass

    def _is(self, archive: ArchiveFileType): ...


factory = ArchiveFactory()
factory.register(None, ArchiveFinder())
