import os
import zipfile
import tarfile
import gzip
from typing import List
from Utilities.base import ArchiverType, ArchiveFileType, ArchiveFindType


class ArchiveFinder(ArchiveFindType):
    """ It finds the proper ArchiverType class in ArchiveFactory """

    def get_val(self, archive: ArchiveFileType) -> ArchiverType:
        return self.factory[self.get_key(archive)]

    def get_key(self, archive: ArchiveFileType) -> str:
        for item, func in self.factory.items():
            if func.combatible_with(archive.pth):
                return item
        else:
            raise KeyError(f"{archive.pth} Format is not compatible")


class GZipper(ArchiveFindType):

    def get_val(self, archive: ArchiveFileType): ...

    def get_key(self, _ignore: ArchiveFileType):
        for key in self.factory:
            if self.factory[key] == self:
                return key

    def warning_decorator(func):
        def wrapper(self, _ignore, *args, **kwargs):
            import warnings

            key = self.get_key(_ignore)
            warnings.warn(f"'{key}' DOES NOT support '{func.__name__}()' method. "
                          f"Try to extract first.",
                          RuntimeWarning, stacklevel=4)
        return wrapper

    @warning_decorator
    def _size_method(self, archive: ArchiveFileType) -> None: ...

    @warning_decorator
    def _inspect_method(self, archive: ArchiveFileType) -> None: ...

    def _extract_method(self, archive: ArchiveFileType):
        with gzip.open(archive.pth, self._r) as f:
            return f.read()

    def _is(self, archive: ArchiveFileType):
        with gzip.GzipFile(archive.pth, self._r) as f:
            try:
                f.read(1)
                return True
            except gzip.BadGzipFile:
                return False


class Zipper(ArchiverType):

    def _extract_method(self, archive: ArchiveFileType):
        with zipfile.ZipFile(archive.pth, self._r) as f:
            f.extractall(path=archive.new, members=archive.mbr, pwd=archive.pwd)

    def _inspect_method(self, archive: ArchiveFileType):
        with zipfile.ZipFile(archive.pth, self._r) as f:
            return f.namelist()

    def _size_method(self, archive: ArchiveFileType):
        result = dict()
        with zipfile.ZipFile(archive.pth) as f:
            for mbr in f.infolist():
                result[mbr.filename] = {'size': mbr.file_size,
                                        'compress': mbr.compress_size}
        return result

    def _is(self, archive: ArchiveFileType):
        return zipfile.is_zipfile(archive.pth)


class TarZipper(ArchiverType):

    def _size_method(self, archive: ArchiveFileType):
        result = dict()
        with tarfile.TarFile(archive.pth, self._r) as f:
            for mbr in f.getmembers():
                if mbr.isfile():
                    result[mbr.name] = {'size': mbr.size}
        return result

    def _inspect_method(self, archive: ArchiveFileType):
        with tarfile.TarFile(archive.pth, self._r) as f:
            return f.getnames()

    def _extract_method(self, archive: ArchiveFileType):
        import warnings

        warnings.warn(f"{self.__class__.__name__} does not use password", RuntimeWarning, stacklevel=4)
        members = self._mbr_to_tar(archive.mbr)
        with tarfile.TarFile(archive.pth, self._r) as f:
            f.extractall(path=archive.pth, members=list(members))

    def _is(self, archive: ArchiveFileType):
        return tarfile.is_tarfile(archive.pth)

    @staticmethod
    def _mbr_to_tar(members) -> List[tarfile.TarInfo]:
        if isinstance(members, (list, tuple)):
            for m in members:
                yield tarfile.TarInfo(os.path.abspath(m))
        else:
            return None
